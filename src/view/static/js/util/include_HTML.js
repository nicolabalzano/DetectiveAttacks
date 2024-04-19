function includeHTML(placeholder_id) {
  /*search for elements with a certain attribute:*/
  const element = document.getElementById(placeholder_id);
  const file_path = element.getAttribute("include-html");
  $(document).ready(function() {
    $("#"+placeholder_id).load(file_path)
  })
}
