jQuery.fn.extend({
    disable: function(state) {
        return this.each(function() {
            var $this = $(this);
            $this.toggleClass('disabled', state);
        });
    },

    error: function(state) {
        return this.each(function() {
            var $this = $(this);
            $this.toggleClass('error', state);
        });
    }
});

function validateEntries(callback) {
    var words = [];

    var validation = true;

    $("#entries input[type=text], #entries textarea").each(function() {
        word = $(this).val();

        console.log(word);

        if (word == "") {
            $(this).error(true);
            validation = false;
        } else {
            $(this).error(false);
            words.push(word);
        }
    });

    callback(validation, words);
}

// Based on the code from:
// https://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format
if (!String.prototype.array_format) {
  String.prototype.array_format = function(arr) {
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof arr[number] != 'undefined'
        ? arr[number]
        : match
      ;
    });
  };
}
