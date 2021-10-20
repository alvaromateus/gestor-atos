var modo = 0 // 0 Edição - 1 Criação

$(document).ready(function() {    
  // Ao mudar setor, tipo ou data aciona método para numeração de documento
  $("input:text:eq(1):visible").focus();
  $("select[name='setor_originario']").change(function() { numero_processo(); });
  $("select[name='tipo']").change(function() { numero_processo(); });
  $("input[name='data_documento']").change(function() { numero_processo(); });
  $("#id_data_documento").click(function(event) { numero_processo(); });

  // Verifica se é create ou edit mode
  if (!document.getElementById("id_numero").value) {  
    modo = 1;  // create mode
    $(".field-status")[0].hidden=true;
    html = '<span class="timezonewarning">Selecione o tipo e o setor originário que a numeração dos Atos será gerada automaticamente.</span>';
    $(".field-tipo").append(html);
    $(".field-atos_revogantes")[0].hidden=true;
    $(".field-atos_alterantes")[0].hidden=true;
  } 
  else {
    desabilita_campos_numeracao(); // edit mode
  }

  // Habilita no submit do edit mode campos desabilitados para edição
  $('form').submit(function(e) {
    $(':disabled').each(function(e) {
        $(this).removeAttr('disabled');
    })
  });

  // Por default desabilita campo de data de supensão de ato
  document.getElementsByClassName("form-row field-data_suspensao")[0].classList.add("hide");

  // Caso o documento possua documentos alteradores ou revogadores mostra documentos
  var id_eh_alterador = document.getElementById("id_eh_alterador");  
  if (id_eh_alterador.checked) {
    document.getElementsByClassName("form-row field-documentos_alterados")[0].classList.remove("hide");
  } else {
    document.getElementsByClassName("form-row field-documentos_alterados")[0].classList.add("hide");
  }  

  var id_eh_revogador = document.getElementById("id_eh_revogador");  
  if (id_eh_revogador.checked) {        
    document.getElementsByClassName("form-row field-documentos_revogados")[0].classList.remove("hide");
    document.getElementsByClassName("form-row field-tipo_revogacao")[0].classList.remove("hide");
  } else {
    document.getElementsByClassName("form-row field-documentos_revogados")[0].classList.add("hide");
    document.getElementsByClassName("form-row field-tipo_revogacao")[0].classList.add("hide");
  }

  var id_status = document.getElementById("id_status").value;  
  if (id_status == 6) { 
    document.getElementsByClassName("form-row field-data_suspensao")[0].classList.remove("hide");
  } else {
    document.getElementsByClassName("form-row field-data_suspensao")[0].classList.add("hide");
  }
});

// Gatilho para mostrar/esconder div documentos se é um ato alterador
$(document).on("change", '#id_status', function() {
  var remember = document.getElementById("id_status").value;
  item = document.getElementsByClassName("form-row field-data_suspensao")[0]
  if (remember == 6) { 
      item.classList.remove("hide");
  } else {
      item.classList.add("hide");
  }
});

// Gatilho para mostrar/esconder div data suspensão documento
$(document).on("change", '#id_eh_alterador', function() {
  var remember = document.getElementById("id_eh_alterador");
  item = document.getElementsByClassName("form-row field-documentos_alterados")[0]
  if (remember.checked) { 
      item.classList.remove("hide");
  } else {
      item.classList.add("hide");
  }        
});

// Gatilho para mostrar/esconder div documentos se é um ato revogador
$(document).on("change", '#id_eh_revogador', function() {
  var remember = document.getElementById("id_eh_revogador");
  documentos_revogados = document.getElementsByClassName("form-row field-documentos_revogados")[0]
  tipo_revogacao = document.getElementsByClassName("form-row field-tipo_revogacao")[0]
  if (remember.checked) {
      documentos_revogados.classList.remove("hide");
      tipo_revogacao.classList.remove("hide");
    } else {
      documentos_revogados.classList.add("hide");
      tipo_revogacao.classList.add("hide");
    }        
});

// Faz a requisição ajax para copular assuntos secundários conforme seleção de assunto principal
$(document).on("change", '#id_assuntos_from', function() {   
  var assuntos = $(this).val();  
  $('select[name="assuntos_secundarios_old"] option:not(:selected)').remove();
  
  if (!(assuntos)) {
    $('select[name="assuntos_secundarios_old"]').prop("disabled", true);
  } else {
    $.ajax({
      url: "/get/ajax/assuntos",
      type: 'get',
      data: {'ids': assuntos },
      success: function(data) {      
        data = JSON.parse(data);
        for (var key in data) {
          $('select[name="assuntos_secundarios_old"]').append(
            $('<option>', {
              value: key,
              text: data[key]
            })
          );
        }        
      }
    });
    $('select[name="assuntos_secundarios_old"]').prop("disabled", false);
  }
});

// desabilita alguns campos no modo de edição
function desabilita_campos_numeracao() {
  $("select[name='tipo']").prop('disabled', true);
  $("select[name='setor_originario']").prop('disabled', true);
  $(".field-data_documento")[0].hidden=true;  
  status_documento = document.getElementById("id_status").value;
  
  // Status exaurido será tratado pela task
  // Status revogado, revogado parcialmente ou alterado é modificado quando é criado um novo documento revogante ou alterante
  switch (status_documento) {
    case '0': { // VIGENTE - remove opções de status que devem ficar indisponíveis 
      $("#id_status option[value='1']").remove();
      $("#id_status option[value='2']").remove();
      $("#id_status option[value='3']").remove();
      $("#id_status option[value='5']").remove();
      $(".field-atos_revogantes")[0].hidden=true;
      $(".field-atos_alterantes")[0].hidden=true;
      console.log('Status vigente.');
      break;
    }
    case '1': { // REVOGADO - remove opções de status que devem ficar indisponíveis     
      document.getElementsByClassName("module aligned")[0].disabled = true;   // desabilita tudo      
      $(document).ready(function() { CKEDITOR.config.readOnly = true; });
  
      $(".field-atos_revogantes")[0].hidden=false;
      $(".field-atos_alterantes")[0].hidden=true;
      data_vigencia(1);
      console.log('Status revogado.');
      break;
    }
    case '2': { // REVOGADO PARCIALMENTE - remove opções de status que devem ficar indisponíveis     
      $("#id_status option[value='0']").remove();
      $("#id_status option[value='1']").remove();
      $("#id_status option[value='3']").remove();      
      $("#id_status option[value='4']").remove();
      $("#id_status option[value='5']").remove();  
      $(".field-eh_revogador")[0].hidden=true;
      $(".field-documentos_revogados")[0].hidden=true;
      $(".field-tipo_revogacao")[0].hidden=true;
      $(".field-eh_alterador")[0].hidden=true;
      $(".field-documentos_alterados")[0].hidden=true;
      
      data_vigencia(2);

      $(".field-atos_revogantes")[0].hidden=false;
      $(".field-atos_alterantes")[0].hidden=true;
      console.log('Status revogado parcialmente.');
      break;
    }
    case '3': { // ALTERADO - remove opções de status que devem ficar indisponíveis
      $("#id_status option[value='0']").remove();
      $("#id_status option[value='1']").remove();
      $("#id_status option[value='2']").remove();      
      $("#id_status option[value='4']").remove();
      $("#id_status option[value='5']").remove();  
      $(".field-eh_revogador")[0].hidden=true;
      $(".field-documentos_revogados")[0].hidden=true;
      $(".field-tipo_revogacao")[0].hidden=true;
      $(".field-eh_alterador")[0].hidden=true;
      $(".field-documentos_alterados")[0].hidden=true;
      data_vigencia(3);
  
      $(".field-atos_revogantes")[0].hidden=true;
      $(".field-atos_alterantes")[0].hidden=false;
      console.log('Status alterado.');
      break;
    }
    case '4': { // SEM EFEITO - remove opções de status que devem ficar indisponíveis
      document.getElementsByClassName("module aligned")[0].disabled = true;   // desabilita tudo      
      $(document).ready(function() { CKEDITOR.config.readOnly = true; });
      data_vigencia(4);
      $(".field-atos_revogantes")[0].hidden=true;
      $(".field-atos_alterantes")[0].hidden=true;
      console.log('Status sem efeito.');
      break;
    }
    case '5': { // EXAURIDO - remove opções de status que devem ficar indisponíveis
      document.getElementsByClassName("module aligned")[0].disabled = true;   // desabilita tudo      
      $(document).ready(function() { CKEDITOR.config.readOnly = true; });
      data_vigencia(5);
      $(".field-atos_revogantes")[0].hidden=true;
      $(".field-atos_alterantes")[0].hidden=true;
      console.log('Status exaurido.');
      break;
    }
    case '6': { // SUSPENSO - remove opções de status que devem ficar indisponíveis
      document.getElementsByClassName("module aligned")[0].disabled = true;   // desabilita tudo      
      $(document).ready(function() { CKEDITOR.config.readOnly = true });      
                  
      data_suspensao = $("#id_data_suspensao").val();
      $(".field-data_suspensao")[0].hidden=true;
      html = '\
        <div style=margin-top:10px;>\
          <hr>\
          <br>\
          <p><b>Data de suspensão:</b> ' + data_suspensao + '</p>\
        <div>';
      $(".field-status").append(html);
      data_vigencia(6);
      console.log('Status suspeenso.');
      $(".field-atos_revogantes")[0].hidden=true;
      $(".field-atos_alterantes")[0].hidden=true;
      break;
    }
    default: {
      $("#id_status").prop('disabled', true);
      $(".field-eh_revogador")[0].hidden=true;
      $(".field-documentos_revogados")[0].hidden=true;
      $(".field-tipo_revogacao")[0].hidden=true;
      $(".field-eh_alterador")[0].hidden=true;
      $(".field-documentos_alterados")[0].hidden=true;
      $(".field-data_inicial")[0].hidden=true;
      $(".field-data_final")[0].hidden=true;
    }
  }
  
}

function data_vigencia(status) {

  data_inicial = $("#id_data_inicial").val();
  if (data_inicial != "") {    
    $(".field-data_inicial")[0].hidden=true;
    html = '\
      <div style=margin-top:10px;>\
        <hr>\
        <br>\
        <p><b>Data do início da vigência:</b> ' + data_inicial + '</p>\
      <div>';
    $(".field-atos_vinculados").append(html);
  }   else {
    $(".field-data_inicial")[0].hidden=true;
  }

  data_final = $("#id_data_final").val();
  if (data_final != "") {
    $(".field-data_final")[0].hidden=true;
    html = '\
      <div style=margin-top:10px;>\
        <hr>\
        <br>\
        <p><b>Data do final da vigência:</b> ' + data_final + '</p>\
      <div>';
    $(".field-atos_vinculados").append(html);
  } else {
    $(".field-data_final")[0].hidden=true;
  }
}

function numero_processo() {
  tipo_ato = document.getElementById("id_tipo").value;
  ano_documento = document.getElementById("id_data_documento").value.split("/")[2];
  setor_originario = document.getElementById("id_setor_originario").value;  
  if (tipo_ato && ano_documento && setor_originario && modo == 1)  {
    $.ajax({
      url: "/get/ajax/numero_documento",
      type: 'get',
      data: {
        'tipo': tipo_ato,
        'ano': ano_documento,
        'setor': setor_originario
      },
      success: function(data) {                  
        $("#id_numero").val(data);
        
        console.log(data);  
      }
    });        
  }
}

function bloquear_form() {
  $("#id_data_documento").prop('disabled', true);  
}