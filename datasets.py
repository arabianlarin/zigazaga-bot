import duckdb
import fpl_api as fa
import fbref as fbr
import pandas as pd

def get_player_data():
    fb = fbr.get_fbref_data()
    players = fa.get_bootstrap().players
    fb['name_norm'] = fb['Player'].apply(fbr.normalize_name)
    players['name_norm'] = players['player_name'].apply(fbr.normalize_name)
    teams = fa.get_teams().teams

    fbref_names = fb['name_norm'].unique()
    players['fbref_match'] = players['name_norm'].apply(lambda x: fbr.fuzzy_match(x, fbref_names))

    mask = (players['fbref_match'].isna()) & (players['minutes'] != 0)

    players.loc[mask, 'name_norm'] = players.loc[mask, 'name_norm'].apply(fbr.shorten_name)

    #players[(players.player_name=='João Pedro Ferreira da Silva') & (players.team==16)]['fbref_match'] == 'Jota'
    players.loc[(players.player_name=='João Pedro Ferreira da Silva') & (players.team==16), 'fbref_match'] = 'Jota'
    players.loc[(players.player_name=='Amara Nallo'), 'fbref_match'] = 'Amara Nallo'
    
    manual_map = {
    'fabio freitas': 'fabio carvalho',
    'alisson becker': 'alisson',
    'jose malheiro': 'jose sa',
    'carlos henrique': 'casemiro',
    'jair paula': 'jair cunha',
    'joao maria': 'joao palhinha',
    'mateus goncalo': 'mateus fernandes',
    'francisco evanilson': 'evanilson',
    'andre trindade': 'andre',
    'estevao almeida': 'estevao willian',
    'norberto bercique': 'beto',
    'felipe rodrigues': 'morato',
    'kevin santos': 'kevin',
    'savio moreira': 'savio',
    'lucas tolentino': 'lucas paqueta',
    'joao victor': 'joao gomes',
    'rodrigo rodri': 'rodri',
    'richarlison de': 'richarlison',
    'joelinton cassio': 'joelinton',
    'bernardo mota': 'bernardo silva',
    'nico gonzalez': 'nicolas gonzalez',
    'igor julio': 'igor',
    'florentino ibrain': 'florentino luis',
    'yeremy pino': 'yeremi pino',
    'ruben dos': 'ruben dias',
    'murillo costa': 'murillo',
    'emiliano buendia': 'emi buendia',
    'matheus santos': 'matheus cunha',
    'andrey nascimento': 'andrey santos',
    'igor thiago': 'thiago'
    }

    players['name_norm'] = players['name_norm'].replace(manual_map)
    #fixtures = fa.get_fixtures()

    full_data = duckdb.query('''
    select
    *
    from players pha
    left join teams t on pha.team = t.id
    --left join fixtures f on t.short_name = f.Team
    left join fb fpd on coalesce(pha.fbref_match, pha.name_norm) = fpd.name_norm-- and t.name = fpd.Squad
    '''
    ).to_df()

    full_data["photo"] = full_data["photo"].str.replace(".jpg", ".png", regex=False)
    full_data['now_cost'] = full_data['now_cost']/10
    full_data['selected_by_percent'] = full_data['selected_by_percent'].astype(float)
    full_data['defensive_contribution_per_90'] = round(full_data['defensive_contribution']/90, 2)
    full_data['CBIT/90'] = round(full_data['TklW_Tackles'] + full_data['Blocks_Blocks'] + full_data['Int'] + full_data['Clr'], 2)
    full_data['Tackles Won %'] = round(full_data['TklW_Tackles']*100/full_data['Tkl_Tackles'], 2)
    full_data['Shots on Target %'] = round(full_data['SoT_per_90_Standard']/full_data['Sh_per_90_Standard'] * 100, 2)
    full_data['diff'] = round(full_data['G_minus_PK'] - full_data['npxG_Expected'], 2)

    return full_data.fillna(0)
