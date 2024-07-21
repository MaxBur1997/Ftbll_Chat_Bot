import requests
from bs4 import BeautifulSoup
from transliterate import translit
from champ_translit import *
from clubs_translit import *


def pars(champ, home, guest):
    if champ == "Ла Лига":
        champ_tag = la_liga
    if champ == "АПЛ":
        champ_tag = apl
    if champ == "Бундеслига":
        champ_tag = bundes
    if champ == "Серия А":
        champ_tag = seria_a

    home_tag = "barcelona"
    guest_tag = "valencia"

    home_req = requests.get(f"https://www.sports.ru/football/club/{home_tag}/calendar/2023-2024/{champ_tag}/")
    guest_req = requests.get(f"https://www.sports.ru/football/club/{guest_tag}/calendar/2023-2024/{champ_tag}/")
    table_req = requests.get(f"https://www.sports.ru/football/tournament/{champ_tag}/table/")
    pvp_req = requests.get("https://www.sports.ru/football/match/1675712/")
    #pvp_req = requests.get(f"https://www.sports.ru/football/match/{home_tag}-vs-{guest_tag}/")
    all_pvp_req = requests.get(f"https://www.sports.ru/football/club/{home_tag}/calendar/2023-2024/")

    home_src = home_req.text
    guest_src = guest_req.text
    table_src = table_req.text
    pvp_src = pvp_req.text
    all_pvp_src = all_pvp_req.text

    home_soup = BeautifulSoup(home_src, 'lxml')
    guest_soup = BeautifulSoup(guest_src, 'lxml')
    table_soup = BeautifulSoup(table_src, 'lxml')
    pvp_soup = BeautifulSoup(pvp_src, 'lxml')
    all_pvp_soup = BeautifulSoup(all_pvp_src, 'lxml')

    games_home = home_soup.find_all("td", string=["Дома", 'В гостях'])
    games_home_num = len(games_home)
    home_games_home = home_soup.find_all("td", string="Дома")
    home_games_home_num = len(home_games_home)

    games_guest = guest_soup.find_all("td", string=["Дома", 'В гостях'])
    games_guest_num = len(games_guest)
    guest_games_guest = guest_soup.find_all("td", string="В гостях")
    guest_games_guest_num = len(guest_games_guest)

    win_games_home = 0
    lose_games_home = 0
    draw_games_home = 0

    for h_game in home_games_home:
        w_result = h_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot gr-dot"})
        if w_result != None:
            win_games_home += 1
        l_result = h_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot rd-dot"})
        if l_result != None:
            lose_games_home += 1
        d_result = h_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot yw-dot"})
        if d_result != None:
            draw_games_home += 1

    win_games_guest = 0
    lose_games_guest = 0
    draw_games_guest = 0

    for g_game in guest_games_guest:
        w_result = g_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot gr-dot"})
        if w_result != None:
            win_games_guest += 1
        l_result = g_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot rd-dot"})
        if l_result != None:
            lose_games_guest += 1
        d_result = g_game.find_next_sibling().find_next_sibling().find("a", {"class": "dot yw-dot"})
        if d_result != None:
            draw_games_guest += 1

    home_scores = win_games_home*3 + draw_games_home
    guest_scores = win_games_guest*3 + draw_games_guest

    home_pos = table_soup.find("a", {'class': 'name'}, string=f"{home}").find_parent('td').find_previous_sibling().text
    guest_pos = table_soup.find("a", {'class': 'name'}, string=f"{guest}").find_parent('td').find_previous_sibling().text

    sup_home = pvp_soup.find("div", string=' Не принимают участие ')

    if sup_home != None:
        home_injuries = sup_home.find_parent().find_all('use',{'xlink:href': '#injury'})
        home_disqualifications = sup_home.find_parent().find_all('use', {'xlink:href': '#disqualification'})
        guest_injuries = sup_home.find_parent().find_next_sibling().find_all('use', {'xlink:href': '#injury'})
        guest_disqualifications = sup_home.find_parent().find_next_sibling().find_all('use', {'xlink:href': '#disqualification'})
        home_inj_num = len(home_injuries)
        home_disq_num = len(home_disqualifications)
        guest_inj_num = len(guest_injuries)
        guest_disq_num = len(guest_disqualifications)
    else:
        home_inj_num = 0
        home_disq_num = 0
        guest_inj_num = 0
        guest_disq_num = 0

    all_pvp = all_pvp_soup.find_all("a", {"title": f"{guest}"}, string=f'{guest}')

    goals = 0
    miss = 0

    for pvp in all_pvp:
        score = pvp.find_parent('td').find_next_sibling('td', {'class': 'score-td'}).find('b').text
        check = pvp.find_parent('td').find_next_sibling('td', {'class': 'alRight padR20'}).text
        if check == "Дома":
            goals += int(score[0])
            miss += int(score[4])
        else:
            goals += int(score[4])
            miss += int(score[0])


    games = {"Матчи хозяев": games_home_num, "Матчи гостей": games_guest_num,
             "Домашние матчи хозяев": home_games_home_num, "Гостевые матчи гостей": guest_games_guest_num,
             "Хозяева выйграли": win_games_home, "Хозяева проиграли": lose_games_home, "Ничья хозяев": draw_games_home,
             "Гости выйграли": win_games_guest, "Гости проиграли": lose_games_guest, "Ничья гостей": draw_games_guest,
             "Очки хозяев": home_scores, "Очки гостей": guest_scores}

    results_of_pars = [home_inj_num, home_disq_num, guest_inj_num, guest_disq_num, home_pos, guest_pos,
                       home_scores, guest_scores, games_home_num, games_guest_num,
                       home_games_home_num, guest_games_guest_num, win_games_home, lose_games_home,
                       draw_games_home, win_games_guest, lose_games_guest, draw_games_guest,
                       goals, miss]

    return results_of_pars
