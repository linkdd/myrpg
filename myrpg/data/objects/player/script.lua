function collision_with_enemy(obj, enemy)
    if obj.data['state'] == 'attacking'
    then
        enemy.data['health'] = enemy.data['health'] - obj.data['damage']
    else
        obj.data['health'] = obj.data['health'] - enemy.data['damage']
    end
end

function collision_with_item(obj, item)
    table.insert(obj.data['inventory'], item)
    item.delete()
end

function collision(obj, other)
    handlers = {
        ['enemy'] = collision_with_enemy,
        ['item'] = collision_with_item
    }

    if handlers[other.type] ~= nil
    then
        handlers[other.type](obj, other)
    end
end
