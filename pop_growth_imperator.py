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


pop_growth_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\pop_growth_modifiers.txt"
travel_time_modifers_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\common\\modifiers\\travel_time_modifiers.txt"
pop_growth_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\pop_growth_events.txt"
travel_time_event_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\Realistic_Growth\\events\\travel_time_events.txt"
localization_file = "F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\localization\\english\\pop_growth_l_english.yml"

modifier_output = ''

levels = [str(x)[:5] for x in range(-100, -10)] + [str(0.1 * x)[:5] for x in range(-100, -15)] + [str(0.01 * x)[:5] for x in range(-150, 151)] + [str(0.1 * x)[:5] for x in range(16, 250)]
food_levels = [str(0.01 * x)[:5] for x in range(1001)]
mig_levels = [str(0.25 * x)[:5] for x in range(-200, 201)]
travel_levels = [str(0.5 * x)[:5] for x in range(201)]


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
            name = civilization_factor
            value = civilization_factor
        }
        set_variable = {
            name = crop_yield_modifier
            value = crop_yield_modifier
        }
        set_variable = {
            name = effective_population
            value = effective_population
        }
'''
    
def binary_search_output(levels, indentation, modifier_prefix, variable):
    if len(levels) > 1:
        middle_level = levels[int(len(levels)/2)]
        first_half, second_half = levels[:int(len(levels)/2)], levels[int(len(levels)/2):]
        output = '\n'+'\t'*indentation + 'if = { limit = {'+variable+'<'+middle_level+' }'
        output += binary_search_output(first_half, indentation+1, modifier_prefix, variable)
        output += '\n'+'\t'*indentation + '}'
        output += '\n'+'\t'*indentation + 'else = { '
        output += binary_search_output(second_half, indentation+1, modifier_prefix, variable)
        output += '\n'+'\t'*indentation + '}'
    else:
        level_name = levels[0].replace('.', '_').replace('-','n')
        output = '\n'+'\t'*indentation + 'add_permanent_province_modifier = { name = '+modifier_prefix+level_name+'}'
    return output
                     
for level_num in range(len(levels)):
    level = levels[level_num]
    level_name = level.replace('.', '_').replace('-','n')
    event_output += '\n\t\tif = {limit = {has_province_modifier = pop_growth'+level_name+'} remove_province_modifier = pop_growth'+level_name+'}'

event_output += binary_search_output(levels, 2, 'pop_growth', 'growth_rate')
        

for level_num in range(len(food_levels)):
    level = food_levels[level_num]
    level_name = level.replace('.', '_').replace('-','n')
    event_output += '\n\t\tif = {limit = {has_province_modifier = surplus_produced'+level_name+'} remove_province_modifier = surplus_produced'+level_name+'}'
event_output += binary_search_output(food_levels, 2, 'surplus_produced', 'surplus_produced')
        
for level_num in range(len(mig_levels)):
    level = mig_levels[level_num]
    level_name = level.replace('.', '_').replace('-','n')
    event_output += '\n\t\tif = {limit = {has_province_modifier = migration_attraction'+level_name+'} remove_province_modifier = migration_attraction'+level_name+'}'
event_output += binary_search_output(mig_levels, 2, 'migration_attraction', 'migration_attraction')

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

modifier_output = ''
for level in travel_levels:
    level_name = level.replace('.', '_').replace('-','n')
    modifier = "travel_time" + level_name + ' = {'
    modifier += "\n\tlocal_tax_modifier = "+str(1 - float(level)/100)
    modifier += "\n\tlocal_manpower_modifier = "+str(1 - float(level)/100)
    modifier += "\n\tlocal_commerce_value_modifier = "+str(1 - float(level)/100)
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
                            value = 0.5
                        }
                        change_variable = {
                            name = additional_travel_time
                            multiply = overextension_factor
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
                            value = 0.5
                        }
                        change_variable = {
                            name = additional_travel_time
                            multiply = overextension_factor
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
            if = {
                limit = { 
                    is_port = yes    
                    NOT = {owner = var:cached_owner} 
                }
                set_variable = {
                    name = cached_owner
                    value = owner
                }
                owner = {
                    set_variable = {
                        name = sea_refresh_count
                        value = 100
                    }
                }
            }
            set_variable = {
                name = travel_from
                value = this
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
                            name = additional_travel_time
                            multiply = overextension_factor
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
                    value = this
                }
                set_variable = {
                    name = travel_time
                    value = 0
                }
            }
            trigger_event = { id = update_travel_time.9001 }
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

event_output += binary_search_output(travel_levels, 2, 'travel_time', 'var:travel_time')
                    
event_output += '''
    }
}

update_travel_time.9002 = {
	type = province_event
	hidden = yes
	picture = elephant_battle
    
    immediate = {
        every_province = {
            limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes}}
            every_neighbor_province = {
                limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes}}
                debug_log = "Province Neighbor [THIS.GetProvince.GetId()] [PREV.GetProvince.GetId()]"
            }
        }
        every_sea_and_river_zone = {
            limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes}}
            every_neighbor_province = {
                limit = {OR = {terrain = riverine_terrain terrain = ocean terrain = coastal_terrain is_port = yes}}
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
            trigger_event = { id = update_travel_time.9006}
        }
        
        every_province = {
            trigger_event = { id = update_travel_time.9003}
            if = {
                limit = {is_port = yes has_owner = yes}
                set_variable = {
                    name = cached_owner
                    value = owner
                }
            }
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
            limit = { province_id = '''+str(provid)+'''}
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
        if float(travel_time) < 1000:
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
    type = character_event
    hidden = yes
    
    trigger = {num_holdings_owned > 0}
    
    immediate = {
        every_holdings = {
            root = {add_gold = gold_from_holding}
        }
    }
}
'''
    
f = open(travel_time_event_file, 'w', encoding='utf-8')
f.write('\ufeff')
f.write(event_output)
f.close()

localization = 'l_english:'
for level in levels:
    level_name = level.replace('.', '_').replace('-','n')
    localization += '\npop_growth' +level_name+':0 "Natural Population Growth Rate"'
    
for level in food_levels:
    level_name = level.replace('.', '_').replace('-','n')
    localization += '\nsurplus_produced'+level_name+':0 "Food Production by Farmers"'
    
for level in mig_levels:
    level_name = level.replace('.', '_').replace('-','n')
    localization += '\nmigration_attraction'+level_name+':0 "Migration Attraction"'
    
for level in travel_levels:
    level_name = level.replace('.', '_').replace('-','n')
    localization += '\ntravel_time'+level_name+':0 "Travel Time from the Capital"'
        
f = open(localization_file, 'w', encoding='utf-8')
f.write('\ufeff')
f.write(localization)
f.close()


def search_for_path(start, end, max_steps):
    if start==end:
        return [start]
    elif max_steps <= 0:
        return False
    else:
        for next_step in adj_dict[start]:
            path = search_for_path(next_step, end, max_steps-1)
            if path != False:
                return [start] + path
