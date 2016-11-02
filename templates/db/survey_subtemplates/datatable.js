$(document).ready(
  function() {
    var table = $('#survey_table_{{survey.id}}').DataTable({
       dom: 'Bfrtip',
      buttons:['copy', 'csv', 'excel', 'pdf', 'print']
    });
  } 
);
