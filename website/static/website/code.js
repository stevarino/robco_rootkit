// Score results in word: score object. Removed words should have a score of -1.
// Object should be fine as order is not important to state deduction.
var Scores = [];

/*
  Set up event callbacks.
  */
$(function() {
  $("#words").on('input', word_input);
  $("#btn_submit").on('click', btn_submit);
  $("#btn_reset").on('click', btn_reset);
  disable_form();
});

/*
  Handle changes to the word input textearea. This will generate API
  calls.
  */
function word_input(e) {
  Scores = [];
  if ($("#words").val() != "") {
    submit_form();
  } else {
    $("#wordlist").empty();
    disable_form();
  }
}

/*
  Submit button pressed - generate an API call with the feedback
  property modified.
  */
function btn_submit() {
  var i = parseInt($("#correct option:selected").val())
  if (!isNaN(i)) {
    Scores.push({
      word: $("#suggest option:selected").val(),
      feedback: i
    });
    submit_form();
  }
}

function btn_reset() {
  $("#words").val("");
  $("#words").focus();
  word_input();
  build_table([]);
}

// processes the response from the server. This includes calling
// create_word_link and activating/deactivating the appropriate elements.
function process_response(res) {
  $("#wordlist").empty();
  for (var i=0; i<res.words.length; i++) {
    // create_word_link(res.words[i]);
  }

  if (! res.valid) {
    disable_form();
  } else {
    $("#correct").removeAttr("disabled");
    $("#correct_mask").removeClass("disabled");
    $("#btn_submit").removeAttr("disabled");
    $("#btn_reset").removeAttr("disabled");
    $("#correct").removeAttr("disabled");
    $("#suggest select").removeAttr("disabled");

    $("#suggest select").empty();

    // build word choice select
    var word = "";
    for (i in res.words) {
      word = res.words[i].word;
      if (res.words[i].valid) {
        $("#suggest select").append(
          $("<option>")
            .attr("value", word)
            .text(word)
        );
      }
    }

    // build feedback select box
    $("#correct").empty();
    $("#correct").append(
      $("<option>").attr("value", -1).text("DEL")
    );
    for (var i=0; i<=word.length; i++) {
      var opt = $("<option>").attr("value", i).text(i)
      if (i == 0) {
        opt.attr("selected", "selected");
      }
      $("#correct").append(opt);
    }
  }

  build_table(res.words);

  // message
  if (res.message !== undefined) {
    $("#message").text(res.message);
  } else {
    $("#message").html("&nbsp;");
  }
}

function build_table(words) {
  // table
  $("table tbody").empty();
  for (var i=0; i<words.length; i++) {
    var td_w = $("<td>").text(words[i].word)
    if (! words[i].valid) {
      td_w.addClass('invalid');
    }
    var td_s = $("<td>");
    if ('score' in words[i]) {
      td_s.text(words[i].score);
    }
    var tr = $("<tr>");
    tr.append(td_w);
    tr.append(td_s);
    tr.append($("<td>").text(words[i].position))
    $("tbody").append(tr);
  }
}

// submits the form data to the api.
function submit_form() {
  $.post("api", JSON.stringify({
    'words': $("#words").val(),
    'feedback': Scores
  }), process_response);
}

// resets the form to ensure ready for new input.
function disable_form() {
  $("#correct").attr("disabled", "disabled");
  $("#correct_mask").addClass("disabled");
  $("#btn_submit").attr("disabled", "disabled");
  $("#btn_reset").attr("disabled", "disabled");
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
    o.feedback = Scores;
    return o;
};
