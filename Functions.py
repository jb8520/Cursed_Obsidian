def Configuration_Position(Guild):
    if Guild==933896845644689449:
        Position=0
    elif Guild==1106689170585432076:
        Position=1
    return Position

def Guild_Id(Position):
    if Position==0:
        Guild=933896845644689449
    elif Position==1:
        Guild=1106689170585432076
    return Guild

def Queue_Display(interaction):
    Message=""
    for i in range(len(interaction.client.Queue_List[Configuration_Position(interaction.guild.id)])):
        if interaction.guild.get_member(interaction.client.Queue_List[Configuration_Position(interaction.guild.id)][i]) is not None:
            Message+=f"\n{i+1}. {interaction.guild.get_member(interaction.client.Queue_List[Configuration_Position(interaction.guild.id)][i]).mention} | {interaction.client.Activity_List[Configuration_Position(interaction.guild.id)][i]} | {interaction.client.Timestamp_List[Configuration_Position(interaction.guild.id)][i]}"
        else:
            interaction.client.Queue_List[Configuration_Position(interaction.guild.id)].pop(i)
            interaction.client.Activity_List[Configuration_Position(interaction.guild.id)].pop(i)
            interaction.client.Timestamp_List[Configuration_Position(interaction.guild.id)].pop(i)
    return Message