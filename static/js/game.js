var current_quiz_id;

function escapeHtml(str) {
    return str
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#x27;");
 }

function stringifyWithSpaces(obj) {
	var result = JSON.stringify(obj, null, 1);
	result = result.replace(/^ +/gm, " ");
	result = result.replace(/\n/g, "");
	result = result.replace(/{ /g, "{").replace(/ }/g, "}");
	result = result.replace(/\[ /g, "[").replace(/ \]/g, "]");
	return result;
}


$( function() {
 $( "#quotations" ).sortable();
 $( "#quotations" ).disableSelection();
} );

var author;

function confirm_delete(){
  if(confirm("Permanently delete account and all associated details.")){
    var url = "/delete_account";
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", url, true);
    xhr.send(null);
    xhr.onreadystatechange = function(){
      if(xhr.readyState == 4 && xhr.status == 200){
        var nextUrl = xhr.responseText;
        window.location.href = nextUrl;
      }
    };
  }
}

function populate_quotes(name){
  var url = "/populate_quotes/" + name;
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.send(null);
  xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
      var intext = xhr.responseText;
      var in_json = JSON.parse(intext);
      current_quiz_id = parseInt(in_json.quiz_id);
      
      $("#item1").html(in_json.sentences[0]);
      $("#item2").html(in_json.sentences[1]);

      $("#source1").html(in_json.works[0]);
      $("#source2").html(in_json.works[1]);

      $('#user_greeting').text(in_json.username);

      if(in_json.account_type == 0){
        $('#signup_prompt').show();
      }else{
        $('#signup_prompt').hide();
      }

    }
  };

  $.each($('#quotations').find('li'), function(){
    $(this).css('border', 'solid 1px #cccccc');
  });

  $('#submit_button').show();
  $('#submit_button').focus();
  $('#next_button').hide();

  $('#quotations').sortable('enable');

  //to avoid user confusion only show a score when a quiz has been submitted
  $('#current_score_val').text('');
}

function start_game(){
  $("#options").hide();
  author = $("#author_select").val();
  populate_quotes(author);
  $("#author_name").append(author);
  $("#game").show();
  $('#submit_button').focus();
}

function submit_answer(){
  var all_works = new Array(escapeHtml($('#source1').html()), escapeHtml($('#source2').html()));
  
  var all_sentences = [];

  $.each($('#quotations').find('li'), function(){
    all_sentences.push(escapeHtml($(this).html()));
  });
  attempt = {"works": all_works};
  attempt["sentences"] = all_sentences;
  grading(stringifyWithSpaces(attempt));
}

function grading(text){
  var url = "/grade_quiz/" + current_quiz_id;
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.send(text);

  xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
      var intext = xhr.responseText;
      var in_json = JSON.parse(intext);

      $('#current_score_val').text(in_json.score);
      $('#total_score_val').text(in_json.total_score);
      $('#current_percent_val').text(in_json.percent);

      var ans_index = 0;
      $.each($('#quotations').find('li'), function(){
        if(in_json.answers[ans_index] == true){
          $(this).css('border', 'green solid 3px');
        }else{
          $(this).css('border', 'red solid 3px');
        }
        ans_index++;
      });
    }
  };
  $('#next_button').show();
  $('#next_button').focus();
  $('#submit_button').hide();

  $('#quotations').sortable('disable');
}

function next_quiz(){
  populate_quotes(author);
}