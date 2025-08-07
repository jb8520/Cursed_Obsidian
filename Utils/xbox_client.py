from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET

from aiohttp import ClientResponseError
from pydantic import ValidationError


from . import XboxApiWrapperError



class XboxClientWrapper():
    def __init__(self, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, tokens_path = 'tokens.json'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tokens_path = tokens_path
        
        self.authentication_manager = None
        self.xbox_client = None
    

    async def initialize(self):
        async with SignedSession() as session:
            self.authentication_manager = AuthenticationManager(
                client_session = session,
                client_id = self.client_id,
                client_secret = self.client_secret,
                redirect_uri = ''
            )

            # Load tokens from file if available
            try:
                with open(self.tokens_path, 'r') as f:
                    tokens = f.read()
                    self.authentication_manager.oauth = OAuth2TokenResponse.model_validate_json(tokens)
            
            except (FileNotFoundError, ValidationError):
                print(f'Could not load valid tokens from {self.tokens_path}. Re-authentication required.')                
                raise

            # Refresh tokens, handle failure gracefully
            try:
                await self.authentication_manager.refresh_tokens()
            
            except Exception:
                print('Could not refresh tokens. You might have to delete the tokens file and re-authenticate.')
                raise

            # Save refreshed tokens
            with open(self.tokens_path, 'w') as f:
                f.write(self.authentication_manager.oauth.model_dump_json())

            # Initialize the Xbox client now that we have valid auth
            self.xbox_client = XboxLiveClient(self.authentication_manager)
    
    
    async def get_xbox_profile_by_gamertag(self, xbox_gamertag: str):
        if not self.xbox_client:
            raise RuntimeError('XboxClientWrapper not initialized. Call initialize() first.')
        
        try:
            xbox_profile = await self.xbox_client.profile.get_profile_by_gamertag(gamertag = xbox_gamertag)
            return xbox_profile
        
        except ClientResponseError as e:
            if e.status == 404:
                raise XboxApiWrapperError("❌ Gamertag not found.")
            
            elif e.status == 401:
                raise XboxApiWrapperError("❌ Unauthorized. Token might be invalid or expired.")
            
            else:
                raise XboxApiWrapperError(f"❌ API Error: {e.status} - {e.message}")
    
    async def get_xbox_friends_by_xuid(self, xuid: int):
        if not self.xbox_client:
            raise RuntimeError('XboxClientWrapper not initialized. Call initialize() first.')
        
        try:
            xbox_friends = await self.xbox_client.people.get_friends_by_xuid(xuid = xuid)
            return xbox_friends
        
        except ClientResponseError as e:
            if e.status == 404:
                raise XboxApiWrapperError("❌ XUID not found.")

            elif e.status == 403:
                raise XboxApiWrapperError("❌ Cannot access this user's friends due to privacy settings.")

            elif e.status == 401:
                raise XboxApiWrapperError("❌ Unauthorized. Token might be invalid or expired.")

            else:
                raise XboxApiWrapperError(f"❌ API Error: {e.status} - {e.message}")