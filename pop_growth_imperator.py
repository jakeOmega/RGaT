# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:08:56 2020

@author: jakef
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:27:09 2020

@author: jakef
"""

import numpy as np

run_travel_time = False
run_pop_growth = True
run_state_loyalty = True
run_localization = True
run_character_loyalty = True
run_overextension = True
run_wealth = True
run_troop_maintenance = True

pop_growth_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\pop_growth_modifiers.txt"
state_loyalty_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\state_loyalty_modifiers.txt"
character_loyalty_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\character_loyalty_modifiers.txt"
travel_time_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\travel_time_modifiers.txt"
overextension_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\overextension_modifiers.txt"
wealth_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\wealth_modifiers.txt"
troop_maintenance_modifier_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\troop_maintenance_modifiers.txt"

pop_growth_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\pop_growth_events.txt"
state_loyalty_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\state_loyalty.txt"
character_loyalty_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\character_loyalty.txt"
travel_time_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\travel_time_events.txt"
overextension_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\overextension_events.txt"
wealth_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\wealth_events.txt"
troop_maintenance_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\events\\troop_maintenance_events.txt"

map_mode_goods_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\trade_goods\\travel_time_trade_goods.txt"

localization_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\localization\\english\\pop_growth_l_english.yml"

def binary_search_output(levels, indentation, modifier_prefix, variable, command, pre_modifier = ' = { name = ', post_modifier = '}', mapping_func = lambda x: x):
    if len(levels) > 1:
        middle_level = levels[int(len(levels)/2)]
        first_half, second_half = levels[:int(len(levels)/2)], levels[int(len(levels)/2):]
        output = '\n'+'\t'*indentation + 'if = { limit = {'+variable+'<'+str(mapping_func(float(middle_level)))+' }'
        output += binary_search_output(first_half, indentation+1, modifier_prefix, variable, command, pre_modifier, post_modifier, mapping_func)
        output += '\n'+'\t'*indentation + '}'
        output += '\n'+'\t'*indentation + 'else = { '
        output += binary_search_output(second_half, indentation+1, modifier_prefix, variable, command, pre_modifier, post_modifier, mapping_func)
        output += '\n'+'\t'*indentation + '}'
    else:
        level_name = levels[0].replace('.', '_').replace('-','n')
        output = '\n'+'\t'*indentation + command +  pre_modifier +modifier_prefix+level_name + post_modifier
    return output


modifier_output = ''

levels = [str(x)[:5] for x in range(-100, -10)] + [str(0.1 * x)[:5] for x in range(-100, -15)] + [str(0.01 * x)[:5] for x in range(-150, 151)] + [str(0.1 * x)[:5] for x in range(16, 251)] + [str(1 * x)[:5] for x in range(26, 101)]
food_levels = [str(0.01 * x)[:5] for x in range(1001)] + [str(0.1 * x)[:5] for x in range(101, 1001)]
mig_levels = [str(0.25 * x)[:5] for x in range(-400, 401)]
travel_levels = [str(0.5 * x)[:5] for x in range(201)]
state_loyalty_levels = [str(0.5 * x)[:5] for x in range(201)]
character_loyalty_levels = [str(0.5 * x)[:5] for x in range(201)]
overextension_levels = [str(0.01 * x)[:5] for x in range(-500, 501)]
wealth_levels = [str(1 * x)[:5] for x in range(0, 201)] + [str(10 * x)[:5] for x in range(21, 201)] + [str(100 * x)[:5] for x in range(21, 201)] + [str(1000 * x)[:6] for x in range(21, 201)] + [str(10000 * x)[:7] for x in range(21, 201)]
income_levels = [str(0.001 * x)[:5] for x in range(0, 201)] + [str(0.01 * x)[:5] for x in range(21, 201)] + [str(0.1 * x)[:5] for x in range(21, 201)] + [str(1 * x)[:6] for x in range(21, 201)] + [str(10 * x)[:7] for x in range(21, 201)]
troop_maintenance_levels = [str(0.1 * x)[:5] for x in range(1001)]

trade_goods_output = 'map_mode_null = {color = hsv {0 0 0.5} category = 8}'
for level in range(101):
    level_name = str(level)
    trade_good = "map_mode" + level_name + ''' = {
    color = hsv { ''' + str(0.3333 * (100 - level)/100) +''' 0.9 0.5 }
    category = 8
}'''
    trade_goods_output += '\n' + trade_good
    
f = open(map_mode_goods_file, 'w', encoding='utf-8')
f.write('\ufeff')
f.write(trade_goods_output)
f.close()

if run_pop_growth:
    for level in levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "pop_growth" + level_name + ' = {'
        modifier += "\n\tlocal_population_growth = " + level
        modifier += '\n}'
        modifier_output += '\n' + modifier
        
    for level in food_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "surplus_produced" + level_name + ' = {'
        modifier += "\n\tlocal_monthly_food = " + level
        modifier += '\n}'
        modifier_output += '\n' + modifier
        
    for level in mig_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "migration_attraction" + level_name + ' = {'
        modifier += "\n\tlocal_migration_attraction = " + level
        modifier += '\n}'
        modifier_output += '\n' + modifier
        
    
        
            
    f = open(pop_growth_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=update_pop_growth

update_pop_growth.1 = {
	type = province_event
	hidden = yes
    
    trigger = {has_owner = yes}
	
	immediate = {   
        set_variable = {
            name = annual_growth_rate
            value = annual_growth_rate
        }             
        set_variable = {
            name = low_pop_food_production
            value = low_pop_food_production
        }
        set_variable = {
            name = marginal_food_production
            value = marginal_food_production
        }
        set_variable = {
            name = crop_yield_modifier
            value = crop_yield_modifier
        }
        set_variable = {
            name = farming_population
            value = farming_population
        }
        set_variable = {
            name = wealth_factor
            value = wealth_factor
        }
'''
                     
    for level_num in range(len(levels)):
        level = levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_province_modifier = pop_growth'+level_name+'} remove_province_modifier = pop_growth'+level_name+'}'
    
    event_output += binary_search_output(levels, 2, 'pop_growth', 'growth_rate', 'add_permanent_province_modifier')
            
    
    for level_num in range(len(food_levels)):
        level = food_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_province_modifier = surplus_produced'+level_name+'} remove_province_modifier = surplus_produced'+level_name+'}'
    event_output += binary_search_output(food_levels, 2, 'surplus_produced', 'surplus_produced', 'add_permanent_province_modifier')
            
    for level_num in range(len(mig_levels)):
        level = mig_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_province_modifier = migration_attraction'+level_name+'} remove_province_modifier = migration_attraction'+level_name+'}'
    event_output += binary_search_output(mig_levels, 2, 'migration_attraction', 'migration_attraction', 'add_permanent_province_modifier')
    
    event_output += '''
    }
}
        
update_pop_growth.2 = {
	type = country_event
	hidden = yes
    
    trigger = {tag = ROM}
	
	immediate = { 
        every_province = {
            trigger_event = { id = update_pop_growth.1 }
        }
    }
}
'''

    f = open(pop_growth_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()


if run_troop_maintenance:
    modifier_output = ''
    for level in troop_maintenance_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "troop_maintenance" + level_name + ' = {'
        modifier += "\n\tglobal_manpower_modifier = -" + str(float(level)/100)
        modifier += '\n}'
        modifier_output += '\n' + modifier       
        
    f = open(troop_maintenance_modifier_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=troop_maintenance

troop_maintenance.1 = {
	type = country_event
	hidden = yes
	
	immediate = {   
        set_variable = {
            name = troop_count
            value = 0
        }
        every_army = {
            limit = {
                OR = {
                    AND = {
                        has_commander = yes
                        commander = {is_mercenary = no}
                    }
                    has_commander = no
                }
            }
            root = {
                change_variable ={
                    name = troop_count
                    add = PREV.unit_size
                }
            }
        }'''
                     
    for level_num in range(len(troop_maintenance_levels)):
        level = troop_maintenance_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_country_modifier = troop_maintenance'+level_name+'} remove_country_modifier = troop_maintenance'+level_name+'}'
    
    event_output += binary_search_output(troop_maintenance_levels, 2, 'troop_maintenance', 'troop_maintenance', 'add_country_modifier')
    
    event_output += '''
    }
}'''
    

    f = open(troop_maintenance_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()


if run_state_loyalty:
    modifier_output = ''
    for level in state_loyalty_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "state_loyalty" + level_name + ' = {'
        modifier += "\n\tcity_monthly_state_loyalty = " + str(-0.02 * float(level))
        if float(level) < 50:
            modifier += "\n\tlocal_defensive = " + str(0.02 * float(level) - 1)
        modifier += "\n\tlocal_pop_conversion_speed_modifier = " + str(0.005 * float(level) - 0.25)
        modifier += "\n\tlocal_pop_assimilation_speed_modifier = " + str(0.005 * float(level) - 0.25)
        modifier += '\n}'
        modifier_output += '\n' + modifier       
         
    modifier = "recent_conquest_loyalty = {"
    modifier += "\n\tlocal_unrest = -1000"
    modifier += "\n\tminimum_unrest = -1000"
    modifier += '\n}'
    modifier_output += '\n' + modifier 
        
    f = open(state_loyalty_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=state_loyalty

state_loyalty.1 = {
	type = province_event
	hidden = yes
    
    trigger = {has_owner = yes}
	
	immediate = {   
'''
                     
    for level_num in range(len(state_loyalty_levels)):
        level = state_loyalty_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\t\tif = {limit = {has_province_modifier = state_loyalty'+level_name+'} remove_province_modifier = state_loyalty'+level_name+'}'
    
    event_output += binary_search_output(state_loyalty_levels, 2, 'state_loyalty', 'state.state_level_loyalty', 'add_permanent_province_modifier')
    
    event_output += '''
    }
}

'''
    

    f = open(state_loyalty_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()
    
    
if run_wealth:
    modifier_output = ''
    for level in wealth_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "province_wealth" + level_name + ' = {'
        modifier += "\n\tlocal_migration_attraction = " + str(0.0025 * float(level))
        modifier += '\n}'
        modifier_output += '\n' + modifier  
        
    for level in wealth_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "province_infrastructure" + level_name + ' = {'
        modifier += "\n\tlocal_population_capacity = " + str(0.001 * float(level))
        modifier += "\n\tlocal_building_slot = " + str(int(0.001 * float(level)))
        modifier += '\n}'
        modifier_output += '\n' + modifier  
    
    for level in income_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "province_taxes" + level_name + ' = {'
        modifier += "\n\ttax_income = " + str(float(level))
        modifier += '\n}'
        modifier_output += '\n' + modifier  
         
        
    f = open(wealth_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=province_wealth

province_wealth.1 = {
	type = province_event
	hidden = yes
    
    trigger = {has_owner = yes}
	
	immediate = {   
        if = {
            limit = {NOT = {has_variable = province_wealth}}
            set_variable = {
                name = province_wealth
                value = 0
            }
        }
        if = {
            limit = {NOT = {has_variable = province_infrastructure}}
            set_variable = {
                name = province_infrastructure
                value = 0
            }
        }
        if = {
            limit = {NOT = {has_variable = last_province_wealth}}
            set_variable = {
                name = last_province_wealth
                value = 0
            }
        }
        set_variable = {
            name = cached_province_wealth
            value = var:province_wealth
        }
        set_variable = {
            name = infrastructure_change
            value = province_infrastructure_change
        }
        change_variable = {
            name = province_infrastructure
            add = var:infrastructure_change
        }            
        set_variable = {
            name = taxes_change
            value = taxes_change
        }
        change_variable = {
            name = province_wealth
            add = province_wealth_change
        }
        set_variable = {
            name = taxes_extracted_display
            value = var:taxes_change
        }
        change_variable = {
            name = province_wealth
            subtract = var:taxes_change
        }
        set_variable = {
            name = per_capita_wealth
            value = var:province_wealth
        }
        change_variable = {
            name = per_capita_wealth
            divide = total_population
        }
        set_variable = {
            name = wealth_factor
            value = wealth_factor
        }
        change_variable = {
            name = taxes_change
            multiply = tax_efficiency
        }
        set_variable = {
            name = tax_efficiency_display
            value = tax_efficiency
        }
        change_variable = {
            name = tax_efficiency_display
            multiply = 100
        }
        owner = {
            capital_scope = {
                change_variable = {
                    name = province_wealth
                    add = ROOT.capital_wealth_extraction
                }
            }
        }
        set_variable = {
            name = last_province_wealth
            value = var:cached_province_wealth
        }
    }
}
        
province_wealth.2 = {
	type = province_event
	hidden = yes
    
    trigger = {has_owner = yes}
	
	immediate = {
'''
                     
    for level_num in range(len(wealth_levels)):
        level = wealth_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\t\tif = {limit = {has_province_modifier = province_wealth'+level_name+'} remove_province_modifier = province_wealth'+level_name+'}'
    
    for level_num in range(len(wealth_levels)):
        level = wealth_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\t\tif = {limit = {has_province_modifier = province_infrastructure'+level_name+'} remove_province_modifier = province_infrastructure'+level_name+'}'
    
    for level_num in range(len(income_levels)):
        level = income_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\t\tif = {limit = {has_province_modifier = province_taxes'+level_name+'} remove_province_modifier = province_taxes'+level_name+'}'
   
    event_output += binary_search_output(wealth_levels, 2, 'province_wealth', 'var:province_wealth', 'add_permanent_province_modifier')
    
    event_output += binary_search_output(wealth_levels, 2, 'province_infrastructure', 'var:province_infrastructure', 'add_permanent_province_modifier')
    
    event_output += binary_search_output(income_levels, 2, 'province_taxes', 'var:taxes_change', 'add_permanent_province_modifier')
    
    event_output += '''
    }
}

province_wealth.3 = {
    type = country_event
    hidden = yes
    
    
    immediate = {
        every_province = {
            switch = {
				trigger = trade_goods
				grain           = { set_variable = {name = old_trade_good_mapmode value = 1 }}
				salt            = { set_variable = {name = old_trade_good_mapmode value = 2 }}
				iron            = { set_variable = {name = old_trade_good_mapmode value = 3 }}
				horses          = { set_variable = {name = old_trade_good_mapmode value = 4 }}
				wine            = { set_variable = {name = old_trade_good_mapmode value = 5 }}
				wood            = { set_variable = {name = old_trade_good_mapmode value = 6 }}
				amber           = { set_variable = {name = old_trade_good_mapmode value = 7 }}
				stone           = { set_variable = {name = old_trade_good_mapmode value = 8 }}
				fish            = { set_variable = {name = old_trade_good_mapmode value = 9 }}
				spices          = { set_variable = {name = old_trade_good_mapmode value = 10 }}
				elephants       = { set_variable = {name = old_trade_good_mapmode value = 11 }}
				papyrus         = { set_variable = {name = old_trade_good_mapmode value = 12 }}
				cloth           = { set_variable = {name = old_trade_good_mapmode value = 13 }}
				wild_game       = { set_variable = {name = old_trade_good_mapmode value = 14 }}
				precious_metals = { set_variable = {name = old_trade_good_mapmode value = 15 }}
				steppe_horses   = { set_variable = {name = old_trade_good_mapmode value = 16 }}
				cattle          = { set_variable = {name = old_trade_good_mapmode value = 17 }}
				earthware       = { set_variable = {name = old_trade_good_mapmode value = 18 }}
				dye             = { set_variable = {name = old_trade_good_mapmode value = 19 }}
				fur             = { set_variable = {name = old_trade_good_mapmode value = 20 }}
				olive           = { set_variable = {name = old_trade_good_mapmode value = 21 }}
				leather         = { set_variable = {name = old_trade_good_mapmode value = 22 }}
				base_metals     = { set_variable = {name = old_trade_good_mapmode value = 23 }}
				woad            = { set_variable = {name = old_trade_good_mapmode value = 24 }}
				marble          = { set_variable = {name = old_trade_good_mapmode value = 25 }}
				honey           = { set_variable = {name = old_trade_good_mapmode value = 26 }}
				incense         = { set_variable = {name = old_trade_good_mapmode value = 27 }}
				hemp            = { set_variable = {name = old_trade_good_mapmode value = 28 }}
				vegetables      = { set_variable = {name = old_trade_good_mapmode value = 29 }}
				gems            = { set_variable = {name = old_trade_good_mapmode value = 30 }}
				camel           = { set_variable = {name = old_trade_good_mapmode value = 31 }}
				glass           = { set_variable = {name = old_trade_good_mapmode value = 32 }}
				silk            = { set_variable = {name = old_trade_good_mapmode value = 33 }}
				dates           = { set_variable = {name = old_trade_good_mapmode value = 34 }}
			}
            if = {
                limit = {NOT = {has_variable = per_capita_wealth}}
                set_trade_goods = map_mode_null
            }
            else = {
            '''
    event_output += binary_search_output(list(map(str, range(100, -1, -1))), 4, 'map_mode', 'var:per_capita_wealth', 'set_trade_goods', pre_modifier = ' = ', post_modifier = '', mapping_func = lambda x: 80 - x * 0.8)
    event_output += '''    
            }    
        }
    }
}
            
province_wealth.4 = {
    type = country_event
    hidden = yes
    
    
    immediate = {
        every_province = {
            set_variable = {
                name = plotting_wealth
                value = var:province_wealth
            }
            switch = {
				trigger = trade_goods
				grain           = { set_variable = {name = old_trade_good_mapmode value = 1 }}
				salt            = { set_variable = {name = old_trade_good_mapmode value = 2 }}
				iron            = { set_variable = {name = old_trade_good_mapmode value = 3 }}
				horses          = { set_variable = {name = old_trade_good_mapmode value = 4 }}
				wine            = { set_variable = {name = old_trade_good_mapmode value = 5 }}
				wood            = { set_variable = {name = old_trade_good_mapmode value = 6 }}
				amber           = { set_variable = {name = old_trade_good_mapmode value = 7 }}
				stone           = { set_variable = {name = old_trade_good_mapmode value = 8 }}
				fish            = { set_variable = {name = old_trade_good_mapmode value = 9 }}
				spices          = { set_variable = {name = old_trade_good_mapmode value = 10 }}
				elephants       = { set_variable = {name = old_trade_good_mapmode value = 11 }}
				papyrus         = { set_variable = {name = old_trade_good_mapmode value = 12 }}
				cloth           = { set_variable = {name = old_trade_good_mapmode value = 13 }}
				wild_game       = { set_variable = {name = old_trade_good_mapmode value = 14 }}
				precious_metals = { set_variable = {name = old_trade_good_mapmode value = 15 }}
				steppe_horses   = { set_variable = {name = old_trade_good_mapmode value = 16 }}
				cattle          = { set_variable = {name = old_trade_good_mapmode value = 17 }}
				earthware       = { set_variable = {name = old_trade_good_mapmode value = 18 }}
				dye             = { set_variable = {name = old_trade_good_mapmode value = 19 }}
				fur             = { set_variable = {name = old_trade_good_mapmode value = 20 }}
				olive           = { set_variable = {name = old_trade_good_mapmode value = 21 }}
				leather         = { set_variable = {name = old_trade_good_mapmode value = 22 }}
				base_metals     = { set_variable = {name = old_trade_good_mapmode value = 23 }}
				woad            = { set_variable = {name = old_trade_good_mapmode value = 24 }}
				marble          = { set_variable = {name = old_trade_good_mapmode value = 25 }}
				honey           = { set_variable = {name = old_trade_good_mapmode value = 26 }}
				incense         = { set_variable = {name = old_trade_good_mapmode value = 27 }}
				hemp            = { set_variable = {name = old_trade_good_mapmode value = 28 }}
				vegetables      = { set_variable = {name = old_trade_good_mapmode value = 29 }}
				gems            = { set_variable = {name = old_trade_good_mapmode value = 30 }}
				camel           = { set_variable = {name = old_trade_good_mapmode value = 31 }}
				glass           = { set_variable = {name = old_trade_good_mapmode value = 32 }}
				silk            = { set_variable = {name = old_trade_good_mapmode value = 33 }}
				dates           = { set_variable = {name = old_trade_good_mapmode value = 34 }}
			}
            if = {
                limit = {NOT = {has_variable = province_wealth}}
                set_trade_goods = map_mode_null
            }
            else = {
            '''
    event_output += binary_search_output([str(x) for x in range(100, -1, -1)], 4, 'map_mode', 'var:plotting_wealth', 'set_trade_goods', pre_modifier = ' = ', post_modifier = '', mapping_func=lambda x: np.exp(np.log(2000) * ((100-x)/100) + np.log(5)))
    event_output += '''    
            }    
        }
    }
}
            
province_wealth.5 = {
    type = country_event
    hidden = yes
    
    
    immediate = {
        every_province = {
            set_variable = {
                name = plotting_wealth
                value = var:province_infrastructure
            }
            switch = {
				trigger = trade_goods
				grain           = { set_variable = {name = old_trade_good_mapmode value = 1 }}
				salt            = { set_variable = {name = old_trade_good_mapmode value = 2 }}
				iron            = { set_variable = {name = old_trade_good_mapmode value = 3 }}
				horses          = { set_variable = {name = old_trade_good_mapmode value = 4 }}
				wine            = { set_variable = {name = old_trade_good_mapmode value = 5 }}
				wood            = { set_variable = {name = old_trade_good_mapmode value = 6 }}
				amber           = { set_variable = {name = old_trade_good_mapmode value = 7 }}
				stone           = { set_variable = {name = old_trade_good_mapmode value = 8 }}
				fish            = { set_variable = {name = old_trade_good_mapmode value = 9 }}
				spices          = { set_variable = {name = old_trade_good_mapmode value = 10 }}
				elephants       = { set_variable = {name = old_trade_good_mapmode value = 11 }}
				papyrus         = { set_variable = {name = old_trade_good_mapmode value = 12 }}
				cloth           = { set_variable = {name = old_trade_good_mapmode value = 13 }}
				wild_game       = { set_variable = {name = old_trade_good_mapmode value = 14 }}
				precious_metals = { set_variable = {name = old_trade_good_mapmode value = 15 }}
				steppe_horses   = { set_variable = {name = old_trade_good_mapmode value = 16 }}
				cattle          = { set_variable = {name = old_trade_good_mapmode value = 17 }}
				earthware       = { set_variable = {name = old_trade_good_mapmode value = 18 }}
				dye             = { set_variable = {name = old_trade_good_mapmode value = 19 }}
				fur             = { set_variable = {name = old_trade_good_mapmode value = 20 }}
				olive           = { set_variable = {name = old_trade_good_mapmode value = 21 }}
				leather         = { set_variable = {name = old_trade_good_mapmode value = 22 }}
				base_metals     = { set_variable = {name = old_trade_good_mapmode value = 23 }}
				woad            = { set_variable = {name = old_trade_good_mapmode value = 24 }}
				marble          = { set_variable = {name = old_trade_good_mapmode value = 25 }}
				honey           = { set_variable = {name = old_trade_good_mapmode value = 26 }}
				incense         = { set_variable = {name = old_trade_good_mapmode value = 27 }}
				hemp            = { set_variable = {name = old_trade_good_mapmode value = 28 }}
				vegetables      = { set_variable = {name = old_trade_good_mapmode value = 29 }}
				gems            = { set_variable = {name = old_trade_good_mapmode value = 30 }}
				camel           = { set_variable = {name = old_trade_good_mapmode value = 31 }}
				glass           = { set_variable = {name = old_trade_good_mapmode value = 32 }}
				silk            = { set_variable = {name = old_trade_good_mapmode value = 33 }}
				dates           = { set_variable = {name = old_trade_good_mapmode value = 34 }}
			}
            if = {
                limit = {NOT = {has_variable = province_wealth}}
                set_trade_goods = map_mode_null
            }
            else = {
            '''
    event_output += binary_search_output([str(x) for x in range(100, -1, -1)], 4, 'map_mode', 'var:plotting_wealth', 'set_trade_goods', pre_modifier = ' = ', post_modifier = '', mapping_func=lambda x: np.exp(np.log(400) * ((100-x)/100) + np.log(50)))
    event_output += '''    
            }    
        }
    }
}
            
province_wealth.6 = {
    type = country_event
    hidden = yes
    
    immediate = {
        every_province = {
            switch = {
        		trigger = var:old_trade_good_mapmode
        		1  = {set_trade_goods = grain}
        		2  = {set_trade_goods = salt}
        		3  = {set_trade_goods = iron}
        		4  = {set_trade_goods = horses}
        		5  = {set_trade_goods = wine}
        		6  = {set_trade_goods = wood}
        		7  = {set_trade_goods = amber}
        		8  = {set_trade_goods = stone}
        		9  = {set_trade_goods = fish}
        		10 = {set_trade_goods = spices}
        		11 = {set_trade_goods = elephants}
        		12 = {set_trade_goods = papyrus}
        		13 = {set_trade_goods = cloth}
        		14 = {set_trade_goods = wild_game}
        		15 = {set_trade_goods = precious_metals}
        		16 = {set_trade_goods = steppe_horses}
        		17 = {set_trade_goods = cattle}
        		18 = {set_trade_goods = earthware}
        		19 = {set_trade_goods = dye}
        		20 = {set_trade_goods = fur}
        		21 = {set_trade_goods = olive}
        		22 = {set_trade_goods = leather}
        		23 = {set_trade_goods = base_metals}
        		24 = {set_trade_goods = woad}
        		25 = {set_trade_goods = marble}
        		26 = {set_trade_goods = honey}
        		27 = {set_trade_goods = incense}
        		28 = {set_trade_goods = hemp}
        		29 = {set_trade_goods = vegetables}
        		30 = {set_trade_goods = gems}
        		31 = {set_trade_goods = camel}
        		32 = {set_trade_goods = glass}
        		33 = {set_trade_goods = silk}
        		34 = {set_trade_goods = dates}
        	}
        	remove_variable = old_trade_good_mapmode
        }
    }
}

'''
    

    f = open(wealth_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()
    


if run_travel_time:    
    modifier_output = ''
    for level in travel_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "travel_time" + level_name + ' = {'
        modifier += "\n\tcity_monthly_state_loyalty = "+str(2 - float(level)/50)
        modifier += "\n\tlocal_manpower_modifier = -"+str(float(level)/100)
        modifier += "\n\tlocal_commerce_value_modifier = -"+str(float(level)/100)
        modifier += '\n}'
        modifier_output += '\n' + modifier
        
    f = open(travel_time_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
    
    
    event_output = 'namespace=update_travel_time'
    debug_log = open("E:\\Libraries\\Desktop\\debug.log")
    lines = debug_log.readlines()
    lines_neighbors = [line.split(':')[7] for line in lines if ("Province Neighbor" in line)]
    lines_travel_A = [line.split(':')[7] for line in lines if ("Travel Time A" in line)]
    lines_travel_B = [line.split(':')[7] for line in lines if ("Travel Time B" in line)]
    adj_dict = {}
    travel_dict_A = {}
    travel_dict_B = {}
    for i in range(1, 7908):
        adj_dict[i] = []
        travel_dict_A[i] = '999999'
    for line in lines_neighbors:
        _, _, first, second = line.strip().split()
        first, second = (int(first), int(second))
        if second not in adj_dict[first]:
            adj_dict[first] += [second]
        if first not in adj_dict[second]:
            adj_dict[second] += [first]
    for line in lines_travel_A:
        _, _, _, provid, travel_time = line.split()
        provid = int(provid)
        travel_dict_A[provid] = travel_time
        
    for line in lines_travel_B:
        _, _, _, provid, tag, travel_time = line.split()
        provid = int(provid)
        if tag not in travel_dict_B.keys():
            travel_dict_B[tag] = [[provid, travel_time]]
        else:
            travel_dict_B[tag] += [[provid, travel_time]]
        
                    
    
    for provid in range(1,7908):
        print(provid)
        event_output +='''
update_travel_time.'''+str(provid)+''' = {
	type = province_event
	hidden = yes
    
    trigger = { province_id = 1 }
	immediate = {
'''
        if provid == 1:
            event_output += '''
        every_country = {
            if = {
                limit = {has_variable = sea_refresh_count}
                change_variable = {
                    name = sea_refresh_count
                    subtract = 1
                }
            }
            else = {
                set_variable = {
                    name = sea_refresh_count
                    value = 100
                }
            }
        }
'''
        if len(adj_dict[provid]) > 0:
            event_output += '''
        every_sea_and_river_zone = {
            limit = {province_id = '''+str(provid)+'''}
            save_scope_as = current_province
            every_country = {
                limit = { var:sea_refresh_count > 0 }
                save_scope_as = country
                set_variable = {
                    name = travel_time_'''+str(provid)+'''
                    value = 999999
                }
                set_variable = {
                    name = proposed_travel_time
                    value = 999999
                }
'''
            for neighbor_provid in adj_dict[provid]:
                event_output += '''
                scope:current_province = {
                    every_neighbor_province = {
                        limit = {
                            province_id = '''+str(neighbor_provid)+'''
                            scope:country = {has_variable = travel_time_'''+str(neighbor_provid)+'''}
                        }
                        set_variable = {
                            name = proposed_travel_time
                            value = scope:country.var:travel_time_'''+str(neighbor_provid)+'''
                        }
                        set_variable = {
                            name = additional_travel_time
                            value = 1
                        }
                        change_variable = {
                            name = proposed_travel_time
                            add = var:additional_travel_time
                        }
                        if = {
                            limit = { var:proposed_travel_time < scope:country.var:travel_time_'''+str(provid)+''' }
                            scope:country = {
                                set_variable = {
                                    name = travel_time_'''+str(provid)+'''
                                    value = prev.var:proposed_travel_time
                                }
                            }
                        }
                    }
    
                    every_neighbor_province = {
                        limit = {
                            province_id = '''+str(neighbor_provid)+'''
                            has_variable = travel_time
                            owner = scope:country
                        }
                        set_variable = {
                            name = proposed_travel_time
                            value = var:travel_time
                        }
                        set_variable = {
                            name = additional_travel_time
                            value = 1
                        }
                        change_variable = {
                            name = proposed_travel_time
                            add = var:additional_travel_time
                        }
                        if = {
                            limit = { var:proposed_travel_time < scope:country.var:travel_time_'''+str(provid)+''' }
                            scope:country = {
                                set_variable = {
                                    name = travel_time_'''+str(provid)+'''
                                    value = prev.var:proposed_travel_time
                                }
                            }
                        }
                    }
                }
'''
            event_output += '''
            }
        }'''
        event_output += '''
        every_ownable_province= {
            limit = {
                province_id = '''+str(provid)+'''
                has_owner = yes
            }
            save_scope_as = current_province
            set_variable = {
                name = travel_from
                value = this
            }
            set_variable = {
                name = old_travel_time
                value = var:travel_time
            }
            set_variable = {
                name = travel_time
                value = 999999
            }
            owner = {
                save_scope_as = country'''
        if len(adj_dict[provid]) > 0:            
            for neighbor_provid in adj_dict[provid]:
                event_output += '''
                scope:current_province = {
                    every_neighbor_province = {
                        limit = {
                            province_id = '''+str(neighbor_provid)+'''
                            scope:country = {
                                has_variable = travel_time_'''+str(neighbor_provid)+'''
                            }
                        }
                        set_variable = {
                            name = proposed_travel_time
                            value = scope:country.var:travel_time_'''+str(neighbor_provid)+'''
                        }
                        set_variable = {
                            name = additional_travel_time
                            value = 0.5
                        }
                        change_variable = {
                            name = proposed_travel_time
                            add = var:additional_travel_time
                        }
                        if = {
                            limit = { var:proposed_travel_time < scope:current_province.var:travel_time }
                            scope:current_province = {
                                set_variable = {
                                    name = travel_from
                                    value = prev
                                }
                                set_variable = {
                                    name = travel_time
                                    value = prev.var:proposed_travel_time
                                }
                            }
                        }
                    }
                }'''
        event_output += '''
            }
            every_neighbor_province = {
                limit = {
                    owner = scope:country
                    has_variable = travel_time
                }
                set_variable = {
                    name = proposed_travel_time
                    value = var:travel_time
                }
                scope:current_province = {
                    set_variable = {
                        name = additional_travel_time
                        value = additional_travel_time_sval
                    }
                }
                change_variable = {
                    name = proposed_travel_time
                    add = scope:current_province.var:additional_travel_time
                }
                if = {
                    limit = { var:proposed_travel_time < scope:current_province.var:travel_time }
                    scope:current_province = {
                        set_variable = {
                            name = travel_from
                            value = prev
                        }
                        set_variable = {
                            name = travel_time
                            value = prev.var:proposed_travel_time
                        }
                    }
                }
            }
            if = {
                limit = {is_capital = yes}
                set_variable = {
                    name = travel_from
                    value = THIS
                }
                set_variable = {
                    name = travel_time
                    value = 0
                }
            }
            else_if = {
                limit = {
                    has_variable = travel_from
                    var:travel_from = {has_variable = travel_from}
                    var:travel_from.var:travel_from = THIS}
                set_variable = {
                    name = travel_from
                    value = THIS
                }
                set_variable = {
                    name = travel_time
                    value = 999999
                }
            }
            if  = {
                limit = {NOT = {var:old_travel_time = var:travel_time}}
                trigger_event = { id = update_travel_time.9001 }
            }
            
            
        }
    }
}
        
'''


    event_output +='''
update_travel_time.9001 = {
	type = province_event
	hidden = yes
    immediate = {
'''
     
    for level_num in range(len(travel_levels)):
        level = travel_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_province_modifier = travel_time'+level_name+'} remove_province_modifier = travel_time'+level_name+'}'
    
    event_output += binary_search_output(travel_levels, 2, 'travel_time', 'effective_travel_time', 'add_permanent_province_modifier')
                        
    event_output += '''
    }
}

update_travel_time.9002 = {
	type = province_event
	hidden = yes
	picture = elephant_battle
    
    immediate = {
        every_province = {
            limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes NOT={any_neighbor_province = {NOT = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain}}}}}}
            every_neighbor_province = {
                limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes NOT={any_neighbor_province = {NOT = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain}}}}}}
                debug_log = "Province Neighbor [THIS.GetProvince.GetId()] [PREV.GetProvince.GetId()]"
            }
        }
        every_sea_and_river_zone = {
            limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes NOT={any_neighbor_province = {NOT = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain}}}}}}
            every_neighbor_province = {
                limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes NOT={any_neighbor_province = {NOT = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain}}}}}}
                debug_log = "Province Neighbor [THIS.GetProvince.GetId()] [PREV.GetProvince.GetId()]"
            }
        }'''
    for provid in range(1, 7908):
        event_output += '''
        every_ownable_province = {
            limit = {province_id = '''+str(provid)+''' has_variable = travel_time}
            debug_log = "Travel Time A '''+str(provid)+''' [THIS.GetVariable('travel_time').GetValue()]"
        }'''
    for provid in range(1, 7908):
        event_output += ''' 
        every_country = {
            limit = {has_coasts = yes has_variable = travel_time_'''+str(provid)+''' }
            debug_log = "Travel Time B '''+str(provid)+''' [THIS.GetCountry().GetTag()] [THIS.GetVariable('travel_time_'''+str(provid)+'''').GetValue()]"
        }'''
    event_output += '''
    }
}

update_travel_time.9003 = {
	type = province_event
	hidden = yes
	picture = elephant_battle
    
    trigger = { province_id = 1 }
    
    immediate = {    
'''
    for provid in range(1,7908):
        event_output += '''
        trigger_event = { id = update_travel_time.'''+str(provid)+''' days = {0 90}}'''
    event_output += '''
        trigger_event = { id = update_travel_time.9003 days = 90}
    }
}
            
update_travel_time.9004 = {
	type = country_event
	hidden = yes
	picture = elephant_battle
    fire_only_once = yes
    
    trigger = { tag = ROM }
    
    immediate = {
        every_country = {
            set_variable = {
                name = sea_refresh_count
                value = 0
            }
        }
        set_variable = {
            name = initialization_loops
            value = 0
        }
        if = { limit = {var:initialization_loops = 0} trigger_event = { id = update_travel_time.9005}}
        if = {
            limit = { var:initialization_loops > 0}
            every_country = {
                set_variable = {
                    name = sea_refresh_count
                    value = prev.var:initialization_loops
                }
            }
            trigger_event = { id = update_travel_time.9006}
        }
        
        every_province = {
            trigger_event = { id = update_travel_time.9003}
        }
    }
}
    
update_travel_time.9005 = {
	type = country_event
	hidden = yes
	picture = elephant_battle
    
    trigger = { tag = ROM }
    
    immediate = {    
'''
    for provid in range(1,7908):
        event_output += '''
        every_province = { 
            limit = { province_id = '''+str(provid)+''' has_owner = yes}
            set_variable = {
                name = travel_time
                value = '''+str(travel_dict_A[provid])+'''
            }
            trigger_event = { id = update_travel_time.9001 }
        }'''
    for tag in travel_dict_B.keys():
        print(tag)
        event_output += '''
        every_country = { 
            limit = { tag = '''+str(tag)+'''}'''
        for i in range(len(travel_dict_B[tag])):
            provid = travel_dict_B[tag][i][0]
            travel_time = travel_dict_B[tag][i][1]
            if float(travel_time) < 100:
                event_output += '''
                set_variable = {
                    name = travel_time_'''+str(provid)+'''
                    value = '''+str(travel_time)+'''
                }'''
        event_output += '''
        }'''
    event_output += '''
    }
}
            
update_travel_time.9006 = {
	type = country_event
	hidden = yes
	picture = elephant_battle
    
    trigger = { tag = ROM }
    
    immediate = {    
        every_province = {
            limit = { province_id = 1 }
'''
    for provid in range(1,7908):
        event_output += '''
            trigger_event = { id = update_travel_time.'''+str(provid)+'''}'''
    event_output += '''
        }
        change_variable = { name = initialization_loops subtract=1}
        if = {
            limit = { var:initialization_loops > 0}
            trigger_event = { id = update_travel_time.9006}
        }
    }
}
        
update_travel_time.9007 = {
    type = country_event
    hidden = yes
    
    
    immediate = {
        every_province = {
            switch = {
				trigger = trade_goods
				grain           = { set_variable = {name = old_trade_good_mapmode value = 1 }}
				salt            = { set_variable = {name = old_trade_good_mapmode value = 2 }}
				iron            = { set_variable = {name = old_trade_good_mapmode value = 3 }}
				horses          = { set_variable = {name = old_trade_good_mapmode value = 4 }}
				wine            = { set_variable = {name = old_trade_good_mapmode value = 5 }}
				wood            = { set_variable = {name = old_trade_good_mapmode value = 6 }}
				amber           = { set_variable = {name = old_trade_good_mapmode value = 7 }}
				stone           = { set_variable = {name = old_trade_good_mapmode value = 8 }}
				fish            = { set_variable = {name = old_trade_good_mapmode value = 9 }}
				spices          = { set_variable = {name = old_trade_good_mapmode value = 10 }}
				elephants       = { set_variable = {name = old_trade_good_mapmode value = 11 }}
				papyrus         = { set_variable = {name = old_trade_good_mapmode value = 12 }}
				cloth           = { set_variable = {name = old_trade_good_mapmode value = 13 }}
				wild_game       = { set_variable = {name = old_trade_good_mapmode value = 14 }}
				precious_metals = { set_variable = {name = old_trade_good_mapmode value = 15 }}
				steppe_horses   = { set_variable = {name = old_trade_good_mapmode value = 16 }}
				cattle          = { set_variable = {name = old_trade_good_mapmode value = 17 }}
				earthware       = { set_variable = {name = old_trade_good_mapmode value = 18 }}
				dye             = { set_variable = {name = old_trade_good_mapmode value = 19 }}
				fur             = { set_variable = {name = old_trade_good_mapmode value = 20 }}
				olive           = { set_variable = {name = old_trade_good_mapmode value = 21 }}
				leather         = { set_variable = {name = old_trade_good_mapmode value = 22 }}
				base_metals     = { set_variable = {name = old_trade_good_mapmode value = 23 }}
				woad            = { set_variable = {name = old_trade_good_mapmode value = 24 }}
				marble          = { set_variable = {name = old_trade_good_mapmode value = 25 }}
				honey           = { set_variable = {name = old_trade_good_mapmode value = 26 }}
				incense         = { set_variable = {name = old_trade_good_mapmode value = 27 }}
				hemp            = { set_variable = {name = old_trade_good_mapmode value = 28 }}
				vegetables      = { set_variable = {name = old_trade_good_mapmode value = 29 }}
				gems            = { set_variable = {name = old_trade_good_mapmode value = 30 }}
				camel           = { set_variable = {name = old_trade_good_mapmode value = 31 }}
				glass           = { set_variable = {name = old_trade_good_mapmode value = 32 }}
				silk            = { set_variable = {name = old_trade_good_mapmode value = 33 }}
				dates           = { set_variable = {name = old_trade_good_mapmode value = 34 }}
			}
            if = {
                limit = {NOT = {has_variable = travel_time}}
                set_trade_goods = map_mode_null
            }
            else = {
            '''
    event_output += binary_search_output(list(map(str, range(101))), 4, 'map_mode', 'var:travel_time', 'set_trade_goods', pre_modifier = ' = ', post_modifier = '', mapping_func = lambda x: 100 * (x/100)**2)
    event_output += '''    
            }    
        }
    }
}
            
update_travel_time.9008 = {
    type = country_event
    hidden = yes
    
    immediate = {
        every_province = {
            switch = {
        		trigger = var:old_trade_good_mapmode
        		1  = {set_trade_goods = grain}
        		2  = {set_trade_goods = salt}
        		3  = {set_trade_goods = iron}
        		4  = {set_trade_goods = horses}
        		5  = {set_trade_goods = wine}
        		6  = {set_trade_goods = wood}
        		7  = {set_trade_goods = amber}
        		8  = {set_trade_goods = stone}
        		9  = {set_trade_goods = fish}
        		10 = {set_trade_goods = spices}
        		11 = {set_trade_goods = elephants}
        		12 = {set_trade_goods = papyrus}
        		13 = {set_trade_goods = cloth}
        		14 = {set_trade_goods = wild_game}
        		15 = {set_trade_goods = precious_metals}
        		16 = {set_trade_goods = steppe_horses}
        		17 = {set_trade_goods = cattle}
        		18 = {set_trade_goods = earthware}
        		19 = {set_trade_goods = dye}
        		20 = {set_trade_goods = fur}
        		21 = {set_trade_goods = olive}
        		22 = {set_trade_goods = leather}
        		23 = {set_trade_goods = base_metals}
        		24 = {set_trade_goods = woad}
        		25 = {set_trade_goods = marble}
        		26 = {set_trade_goods = honey}
        		27 = {set_trade_goods = incense}
        		28 = {set_trade_goods = hemp}
        		29 = {set_trade_goods = vegetables}
        		30 = {set_trade_goods = gems}
        		31 = {set_trade_goods = camel}
        		32 = {set_trade_goods = glass}
        		33 = {set_trade_goods = silk}
        		34 = {set_trade_goods = dates}
        	}
        	remove_variable = old_trade_good_mapmode
        }
    }
}
'''
    
    f = open(travel_time_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()

if run_character_loyalty:
    modifier_output = ''
    for level in character_loyalty_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "character_distance" + level_name + ' = {'
#        modifier += "\n\tloyalty = " + str(-0.2 * float(level))
        modifier += "\n\tmonthly_corruption = " + str(0.0025 * float(level))
        modifier += '\n}'
        modifier_output += '\n' + modifier       
        
    f = open(character_loyalty_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=character_loyalty

character_loyalty.1 = {
	type = character_event
	hidden = yes
    
    trigger = { }
	
	immediate = {      
'''
                     
    for level_num in range(len(state_loyalty_levels)):
        level = state_loyalty_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_character_modifier = character_distance'+level_name+'} remove_character_modifier = character_distance'+level_name+'}'
    
    event_output += '''\n\tif = {
        limit = {is_governor = yes}'''
    event_output += binary_search_output(character_loyalty_levels, 3, 'character_distance', 'location.var:travel_time', 'add_character_modifier')
    
    event_output += '''
        }
    }
}'''
    

    f = open(character_loyalty_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()
    
if run_overextension:
    modifier_output = ''
    for level in overextension_levels:
        level_name = level.replace('.', '_').replace('-','n')
        modifier = "overextension_change" + level_name + ' = {'
        modifier += "\n\tagressive_expansion_monthly_change = " + str(float(level))
        modifier += '\n}'
        modifier_output += '\n' + modifier       
        
    f = open(overextension_modifers_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(modifier_output)
    f.close()
            
    event_output = '''namespace=overextension

overextension.1 = {
	type = country_event
	hidden = yes
	
	immediate = {     
        set_variable = {
            name = admin_demand
            value = admin_demand
        }
        set_variable = {
            name = admin_capacity
            value = 100
        }
        every_country_culture = {
            limit = {
                OR = {
					is_culture = ROOT.culture
					is_integrated = yes
				}
            }
            save_scope_as = current_culture
            root = {
                every_owned_province = {
                    every_pops_in_province = {
                        limit = {pop_culture = scope:current_culture.culture}
                        if = {
                            limit = {pop_type = nobles}
                            ROOT = {
                                change_variable = {
                                    name = admin_capacity
                                    add = 10
                                }
                            }
                        }
                        if = {
                            limit = {pop_type = citizen}
                            ROOT = {
                                change_variable = {
                                    name = admin_capacity
                                    add = 2
                                }
                            }
                        }
                    }
                }
            }
        }
'''
                     
    for level_num in range(len(overextension_levels)):
        level = overextension_levels[level_num]
        level_name = level.replace('.', '_').replace('-','n')
        event_output += '\n\t\tif = {limit = {has_country_modifier = overextension_change'+level_name+'} remove_country_modifier = overextension_change'+level_name+'}'
    
    event_output += binary_search_output(overextension_levels, 2, 'overextension_change', 'overextension_change', 'add_country_modifier')
    
    event_output += '''
    }
}'''
    

    f = open(overextension_event_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(event_output)
    f.close()
   

if run_localization:
    localization = 'l_english:'
    for level in levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\npop_growth' +level_name+':0 "Natural Population Growth Rate"'
        localization += '\ndesc_pop_growth' +level_name+':0 "The population growth rate tends towards 3% of the current population per year if the province is well below the population capacity, and decreases to zero (for rural areas) or even negative values (for large cities) near the population capacity."'
        
    for level in food_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\nsurplus_produced'+level_name+':0 "Food Production by Farmers"'
        localization += '\ndesc_surplus_produced'+level_name+':0 "Food is produced by all non-noble pops in the province. The first pop in the province produces the most food, and each additional pop produces a smaller additional amount of food. The effective workforce of non-slave pops is decreased when at low national manpower, and is capped for a city or metropolis. Mouse over the province name for additional information on these values."'
        
    for level in mig_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\nmigration_attraction'+level_name+':0 "Migration Attraction"'
        localization += '\ndesc_migration_attraction'+level_name+':0 "How attractive the province is to migrants. This is higher in rural provinces the higher the marginal food production is, and is higher in cities the further below the population cap the city is."'
        
    for level in travel_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\ntravel_time'+level_name+':0 "Travel Time from the Capital: '+str(level)+'"'
        localization += '\ndesc_travel_time'+level_name+':0 "How long it takes to reach this province from the capital. Each unit of distance causes a 1% penalty in the manpower and cash output of a province. The distance is calculated as 1 (for sea), 1.5 (for farmland, and plains), 3 (for hills, forests, and deserts), or 7.5 (for mountains, marshes, or jungles) per province that must be crossed to get to the capital. Roads cut the movement cost by half (e.g. crossing a hills province only decreases output by 1.5% rather than 3%). Closer provinces are also easier to keep loyal."'
        
    for level in state_loyalty_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\nstate_loyalty'+level_name+':0 "Loyalty Decay"'
        localization += '\ndesc_state_loyalty'+level_name+':0 "Over time, this province will forget all the good we have done for them. However, this decay is typically counteracted by the travel time modifier - the equilibrium loyalty without any other factors will be 100 minus the travel time to the province."'
        
    for level in wealth_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\nprovince_wealth'+level_name+':0 "Local Wealth: '+str(level)+'"'
        localization += '\ndesc_province_wealth'+level_name+':0 "The local wealth in the province in gold."'
        localization += '\nprovince_infrastructure'+level_name+':0 "Local Infrastructure: '+str(level)+'"'
        localization += '\ndesc_province_infrastructure'+level_name+':0 "The local infrastructure in the province, whether it be in tools, buildings, or irrigation canals."'
        
    for level in income_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\nprovince_taxes'+level_name+':0 "Local Tax Income: '+str(level)+'"'
        localization += '\ndesc_province_taxes'+level_name+':0 "How much wealth we are putting into our coffers each month from our taxes on the province."'
        
    for level in overextension_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\noverextension_change'+level_name+''':0 "Administrative Burden: (#R [Player.MakeScope.GetVariable('admin_demand').GetValue|1]#!/#G [Player.MakeScope.GetVariable('admin_capacity').GetValue|1]#!)"'''
        localization += '\ndesc_overextension_change'+level_name+':0 "This is based on the relative values of our administrative capacity and administrative demand. Each noble pop of an integrated culture provides 5 administrative capacity and each citizen of an integrated culture provides 1 administrative capacity. Every pop in our empire costs administrative demand depending on our laws. If our administrative demand is, for example, 50% higher than our administrative capacity, our overextension will tend towards 50."'
        
    for level in troop_maintenance_levels:
        level_name = level.replace('.', '_').replace('-','n')
        localization += '\ntroop_maintenance'+level_name+':0 "Army Maintenance: '+str(level)+'%"'
        localization += '\ndesc_troop_maintenance'+level_name+':0 "This is the proportion of our manpower that is needed to replace our current army as they get too old to fight or die of natural causes."'
        
        
        
            
    f = open(localization_file, 'w', encoding='utf-8')
    f.write('\ufeff')
    f.write(localization)
    f.close()

