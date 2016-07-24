// Score results in word: score object. Removed words should have a score of -1.
// Object should be fine as order is not important to state deduction.
var Scores = {};

$(function() {
  $("#words").on('input', word_input);
  $("#btn_submit").on('click', btn_submit);
  $("#btn_removed").on('click', btn_submit);
  disable_form();
});

function word_input(e) {
  Scores = {};
  if ($("#words").val() != "") {
    var form = $("form").serializeObject();
    $.post("api", JSON.stringify(form), process_response);
  } else {
    $("#wordlist").empty();
    disable_form();
  }
}

function btn_submit() {
  var i = parseInt($("#correct option:selected").val())
  if (!isNaN(i)) {

  }
}

function btn_removed() {

}

// processes the response from the server. This includes calling
// create_word_link and activating/deactivating the appropriate elements.
function process_response(res) {
  $("#wordlist").empty();
  for (var i=0; i<res.words.length; i++) {
    create_word_link(res.words[i]);
  }

  if (res.valid) {
    $("#correct").removeAttr("disabled");
    $("#correct_mask").removeClass("disabled");
    $("#btn_submit").removeAttr("disabled");
    $("#btn_removed").removeAttr("disabled");
    $("#correct").removeAttr("disabled");
    $("#suggest select").removeAttr("disabled");

    $("#suggest select").empty();
    for (var i=0; i<res.words.length; i++) {
      $("#suggest select").append(
        $("<option>")
          .attr("value", res.words[i].word)
          .text(res.words[i].word)
      );
    }

    $("#correct").empty();
    for (var i=0; i<=res.words[0].word.length; i++) {
      $("#correct").append(
        $("<option>").attr("value", i).text(i)
      );
    }

  } else {
    disable_form();
  }
  if (res.message !== undefined) {
    $("#message").text(res.message);
  } else {
    $("#message").text("");
  }
}

// resets the form to ensure ready for new input.
function disable_form() {
  $("#correct").attr("disabled", "disabled");
  $("#correct_mask").addClass("disabled");
  $("#btn_submit").attr("disabled", "disabled");
  $("#btn_removed").attr("disabled", "disabled");
  $("#suggest select").attr("disabled", "disabled");
  $("#suggest select").empty().append("<option></option>");
}

// given a  word, appends it to the #wordlist element.
function create_word_link(word) {
    var link = $("<span>");
    var title = "";
    if (word.score !== undefined) {
      title += "Score: " + word.score + " ";
    }
    if (word.position !== undefined) {
      title += "Position: " + word.position + " ";
    }
    link.text(word.word);
    link.attr('title', title);
    if (word.invalid !== undefined && word.invalid) {
      link.addClass("invalid");
    }

    link.click(function(e) {
      e.preventDefault();

    })
    $("#wordlist").append(link);
    $("#wordlist").append(" &nbsp;");
}

// user clicked number_correct button. Add to Scores object and process.
function number_correct_onclick(e) {

}

// serialize form into json
// http://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jquery
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
