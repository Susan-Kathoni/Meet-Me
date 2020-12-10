$(document).ready(function(){
  $('form').submit(function(event){
    event.preventDefault()
    form = $("form")

    $.ajax({
      'url':'/ajax/newsletter/',
      'type':'POST',
      'data':form.serialize(),
      'dataType':'json',
      'success': function(data){
        alert(data['success'])
      },
    })// END of Ajax method
    $('#id_your_name').val('')
    $("#id_email").val('')
  }) // End of submit event

}) // End of document ready function

document.addEventListener("DOMContentLoaded", function () {
    M.AutoInit();
    let elems = document.querySelectorAll(".collapsible");
    let instances = M.Collapsible.init(elems);
  
    let elements = document.querySelectorAll(".sidenav");
    let instance = M.Sidenav.init(elements);
  
    var elems2 = document.querySelectorAll("select");
    var instances2 = M.FormSelect.init(elems2);
  });