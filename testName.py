get_lck_name = {
  'grf' : 'Griffin',
  'sb' : 'SANDBOX Gaming',
  'gen' : 'Gen.G',
  'jag' : 'Jin Air Green Wings',
  'kz' : 'KINGZONE DragonX',
  'skt' : 'SK Telecom T1',
  'kt' : 'KT Rolster',
  'dwg' : 'DAMWON Gaming',
  'hle' : 'Hanwha Life Esports',
  'af' : 'Afreeca Freecs'
}

get_lec_name = {
  'msf' : 'Misfits',
  'xl' : 'Excel Esports',
  'rge' : 'Rogue',
  'vit' : 'Team Vitality',
  'fnc' : 'Fnatic',
  'og' : 'Origen',
  'g2' : 'G2 Esports',
  'sk' : 'SK Gaming',
  'spy' : 'Splyce',
  's04' : 'Schalke 04'
}

league = 'LCK'

if league == 'LCK':
  get_team_name_from_league = get_lck_name
elif league == 'LEC':
  get_team_name_from_league = get_lec_name
elif league == 'OPL':
  get_team_name_from_league = get_opl_name
elif league == 'LFL':
  get_team_name_from_league = get_lfl_name
elif league == 'LVP':
  get_team_name_from_league = get_lvp_name

given_dates = ['05', '14', '07', '08', '09']
team_1_and_date_string = 'SKT015'
#team_2_string = '+000018:0001:0010:0017:0SKT'
#team_2_string = '+000018:0001:0010:0017:00KT'

for idx, character in enumerate(team_1_and_date_string):
  if team_1_and_date_string[:idx].lower() in get_team_name_from_league:
    team_1 = team_1_and_date_string[:idx].lower() 
    team_1_score = team_1_and_date_string[idx:idx+2][:1]
    team_2_score = team_1_and_date_string[idx:idx+2][1:]
    date_of_match = team_1_and_date_string[idx+2:]
    if int(date_of_match) < 10:
        date_of_match = '0' + team_1_and_date_string[idx+2:]

for idx, character in enumerate(team_2_string):
  if team_2_string[-idx:].lower() in get_team_name_from_league:
     team_2 = team_2_string[-idx:].lower()
     print("matched")


print(team_1)
print(team_2)
print(team_1_score + ' ' + team_2_score)
print(date_of_match)

# if team_1_and_date_string[-2:] in given_dates:
#     print("we gucci")
# else:
#     if int(date_of_match) < 10:
#         date = int(date_of_match)+1
#     else:
#         print("We are gucci after +1")





# ['05', '06', '07', '08', '09']
# ['JAG025', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00KT']
# 2019/06/05 jag kt
# ['GEN215', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00DWG']
# 2019/06/05 gen dwg
# ['SB206', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00HLE']
# 2019/06/06 sb hle
# ['GRF216', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00AF']
# 2019/06/06 grf af
# ['SKT217', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00JAG']
# 2019/06/07 skt jag
# ['KZ207', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00GEN']
# 2019/06/07 kz gen
# ['HLE208', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00KT']
# 2019/06/08 hle kt
# ['DWG028', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00GRF']
# 2019/06/08 dwg grf
# ['SB029', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00KZ']
# 2019/06/09 sb kz
# ['AF219', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00SKT']
# 2019/06/09 af skt
# ['12', '13', '14', '15', '16']
# ['HLE0212', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00AF']
# 2019/06/12 hle af
# ['GRF1212', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00SB']
# 2019/06/12 grf sb
# ['GEN2013', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00JAG']
# 2019/06/13 gen jag
# ['KZ2113', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00SKT']
# 2019/06/13 kz skt
# ['KT1214', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00DWG']
# 2019/06/14 kt dwg
# ['GRF2014', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00HLE']
# 2019/06/14 grf hle
# ['AF2115', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00KZ']
# 2019/06/15 af kz
# ['SKT0215', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00SB']
# 2019/06/15 skt sb
# ['KT2116', 'June', '2019', '08:00:00', '+000018:0001:0010:0017:00GEN']
# 2019/06/16 kt gen
# ['JAG1216', 'June', '2019', '11:00:00', '+000021:0004:0013:0020:00DWG']

# 2019/06/08 s04 xl
# ['XL018', 'June', '2019', '15:00:00', '+000001:0008:0017:0000:00RGE']
# 2019/06/09 xl rge
# ['SK108', 'June', '2019', '16:00:00', '+000002:0009:0018:0001:00S04']
# 2019/06/09 sk s04
# ['SPY108', 'June', '2019', '17:00:00', '+000003:0010:0019:0002:00VIT']
# 2019/06/09 spy vit
# ['MSF018', 'June', '2019', '18:00:00', '+000004:0011:0020:0003:00FNC']
# 2019/06/09 msf fnc
# ['OG018', 'June', '2019', '19:00:00', '+000005:0012:0021:0004:00G2']
# 2019/06/09 og g2
# ['15', '16']
# ['MSF1014', 'June', '2019', '16:00:00', '+000002:0009:0018:0001:00XL']
# 2019/06/15 msf xl
# ['RGE1014', 'June', '2019', '17:00:00', '+000003:0010:0019:0002:00VIT']
# 2019/06/15 rge vit
# ['FNC1014', 'June', '2019', '18:00:00', '+000004:0011:0020:0003:00OG']
# 2019/06/15 fnc og
# ['SPY0114', 'June', '2019', '19:00:00', '+000005:0012:0021:0004:00S04']
# 2019/06/15 spy s04
# ['G21014', 'June', '2019', '20:00:00', '+000006:0013:0022:0005:00SK']
# 2019/06/15 g2 sk
# ['XL0115', 'June', '2019', '15:00:00', '+000001:0008:0017:0000:00SPY']
# 2019/06/16 xl spy
# ['SK1015', 'June', '2019', '16:00:00', '+000002:0009:0018:0001:00RGE']
# 2019/06/16 sk rge
# ['OG1015', 'June', '2019', '17:00:00', '+000003:0010:0019:0002:00MSF']
# 2019/06/16 og msf
# ['S040115', 'June', '2019', '18:00:00', '+000004:0011:0020:0003:00FNC']
# 2019/06/16 s04 fnc
# ['VIT0115', 'June', '2019', '19:00:00', '+000005:0012:0021:0004:00G2']


  #if we add +1 then does it match

  #if not then we add a 0 beforehand and compare again

  #if we still dont match then we +1 to the new one with the added 0
