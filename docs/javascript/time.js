function zeroPad(number, length) {
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
    return str;
}

function iso8601(year, month, day, hour, minutes, seconds) {
  return year+'-'+zeroPad(month,2)+'-'+zeroPad(day,2)
         +'T'+zeroPad(hour,2)+':'+zeroPad(minutes,2)+':'+zeroPad(seconds,2);
}
