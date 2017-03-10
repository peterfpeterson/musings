---
---
###
http://coffeescript.org/
https://coffeescript-cookbook.github.io/
https://www.w3schools.com/jsref/

high level things marked with @ are exported
###
zeroPad = (number, length) ->
    str = '' + number
    str = '0' + str while str.length < length
    return str

formatDate = (year, month, day) ->
    return year+'-'+zeroPad(month,2)+'-'+zeroPad(day,2)

formatTime = (hour, minute, second) ->
    return zeroPad(hour,2)+':'+zeroPad(minute,2)+':'+zeroPad(second,2);

Date::iso8601 = (gmt) ->
     if gmt
        date = formatDate(@getUTCFullYear(), @getUTCMonth()+1, @getUTCDate())
        time = formatTime(@getUTCHours(), @getUTCMinutes(), @getUTCSeconds())
        tzd = 'Z'
     else
        date = formatDate(@getFullYear(), @getMonth()+1, @getDate())
        time = formatTime(@getHours(), @getMinutes(), @getSeconds())
        tzoffset = @getTimezoneOffset()/60
        if tzoffset > 0
          tzoffset = '+'+tzoffset
        tzd = tzoffset+':00';
     return date+'T'+time+tzd


# a lunar second is 29.530589/30.
lunar_factor = 0.9843529666671
#lunar_factor = 0.9843529666666666
#lunar_factor = 1.0158957547375707
###
epoch is when Neil Armstrong set foot on the Moon surface
on July 21th 1969 at 02:56:15 UT or -14144625 seconds
#lunar_epoch = Date.parse("02:56:15 July 21, 1969")/1000
# in seconds
###
#lunar_epoch = -14144625
lunar_epoch = 14140093.381000042

Date::lunar = () ->
    # convert to landing date epoch in loony secs
    s = ((@getTime()/1000)+lunar_epoch)/ lunar_factor
    # funny constants
    m=0x3C
    h=0xE10
    p=0x15180
    d=0x278D00

    # year
    y=0x1DA9C00
    Y=(s/y)|0
    s-=y*(Y++)
    # month
    D=(s/d)|0
    s-=d*(D++)
    # day
    C=(s/p)|0
    s-=p*(C++)
    # hour
    H=(s/h)|0
    # BUG SOMEWHERE HERE
    s-=h*H
    # minute
    M=(s/m)|0
    s-=m*M

    time = formatTime(H, M, (s/1)|0)

    date = formatDate(Y,D,C)

    return date+'&nambla;'+time
