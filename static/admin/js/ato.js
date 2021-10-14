var modo = 0 // 0 Edição - 1 Criação

$(document).ready(function() {    
  $("input:text:eq(1):visible").focus();

  // Ao mudar setor, tipo ou data aciona método para numeração de documento
  $("select[name='setor_originario']").change(function() { numero_processo(); });
  $("select[name='tipo']").change(function() { numero_processo(); });
  $("input[name='data_documento']").change(function() { numero_processo(); });
  $("#id_data_documento").click(function(event) { numero_processo(); });

  // Verifica se é create ou edit mode
  if (!document.getElementById("id_numero").value) {  
    modo = 1;  // create mode
    $(".field-status")[0].hidden=true;    
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
  if (status_documento == 0) { // status igual a 0 deixa alterar, mas remove remove demais opções deixando só sem efeito)    
    // Status exaurido será tratado pela task
    // Status revogado, revogado parcialmente ou alterado é alterado quando é criado um novo documento revogante ou alterante
    $("#id_status option[value='1']").remove();
    $("#id_status option[value='2']").remove();
    $("#id_status option[value='3']").remove();
    $("#id_status option[value='5']").remove();
  } else { // demais status desabilita a opção de alteração de status
    $("#id_status").prop('disabled', true);    
    $("#id_status").prop('disabled', true);    
    
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