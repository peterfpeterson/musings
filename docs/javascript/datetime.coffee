---
---
zeroPad = (number, length) ->
    str = '' + number
    str = '0' + str while str.length < length
    return str

formatDate = (year, month, day) ->
    return year+'-'+zeroPad(month,2)+'-'+zeroPad(day,2)

formatTime = (hour, minute, second) ->
    return zeroPad(hour,2)+':'+zeroPad(minute,2)+':'+zeroPad(second,2);

class @DateTime extends Date
  constructor: () ->
    @datetime = new Date()

  iso8601: (gmt) ->
     if gmt
        date = formatDate(@datetime.getUTCFullYear(), @datetime.getUTCMonth()+1, @datetime.getUTCDate())
        time = formatTime(@datetime.getUTCHours(), @datetime.getUTCMinutes(), @datetime.getUTCSeconds())
        tzd = 'Z'
     else
        date = formatDate(@datetime.getFullYear(), @datetime.getMonth()+1, @datetime.getDate())
        time = formatTime(@datetime.getHours(), @datetime.getMinutes(), @datetime.getSeconds())
        tzoffset = @datetime.getTimezoneOffset()/60
        if tzoffset > 0
          tzoffset = '+'+tzoffset
        tzd = tzoffset+':00';
     return date+'T'+time+tzd
