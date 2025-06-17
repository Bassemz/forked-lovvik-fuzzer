


def showProperties(characteristic) :
    ret=''
    if(characteristic.readable()) : ret+='r'
    if(characteristic.writeable()) : ret+='w'
    if(characteristic.can_notify()) : ret+='n'
    return ret
