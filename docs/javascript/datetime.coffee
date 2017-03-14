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

Date::decimal = (local) ->
    if local
        date = formatDate(@getFullYear(), @getMonth()+1, @getDate())
        seconds = @getSeconds() + 60 * (@getMinutes() + 60 * @getHours())
    else
        date = formatDate(@getUTCFullYear(), @getUTCMonth()+1, @getUTCDate())
        seconds = @getUTCSeconds() + 60 * (@getUTCMinutes() + 60 * @getUTCHours())

    seconds = ''+(seconds/100000)

    return date+seconds.substr(1,5)

Date::zoneAbbr = () ->
    return String(@).split("(")[1].split(")")[0]

Date::week = (gmt) ->
    if gmt
        onejan = new Date(@getUTCFullYear(), 0, 1)
    else
        onejan = new Date(@getFullYear(), 0, 1)
    return Math.ceil((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7)
