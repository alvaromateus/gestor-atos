// Faz a requisição ajax para numeração automática de documentos
$(document).ready(function() {
  $("select[name='setor_originario']").change(function() {
    numero_processo();
  });
});

$(document).ready(function() {
  $("select[name='tipo']").change(function() {
    numero_processo();
  });
});

$(document).ready(function() {
  $("input[name='data_documento']").change(function() {
    numero_processo();
  });
});
$(document).ready(function() {
  $("#id_data_documento").click(function(event) {
    numero_processo();
  });
});

function numero_processo() {
  tipo_ato = document.getElementById("id_tipo").value;
  ano_documento = document.getElementById("id_data_documento").value.split("/")[2];
  setor_originario = document.getElementById("id_setor_originario").value;
  if (tipo_ato && ano_documento && setor_originario)  {
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

// Verifica se documento possui documentos revogados e/ou alterados para mostrar div
window.onload = function() {
    var id_eh_alterador = document.getElementById("id_eh_alterador");
    var id_eh_revogador = document.getElementById("id_eh_revogador");
    
    if (id_eh_alterador.checked) {
        document.getElementsByClassName("form-row field-documento_alterado")[0].classList.remove("hide");
      } else {
        document.getElementsByClassName("form-row field-documento_alterado")[0].classList.add("hide");
      }      
    if (id_eh_revogador.checked) {        
        document.getElementsByClassName("form-row field-documento_revogado")[0].classList.remove("hide");
        document.getElementsByClassName("form-row field-tipo_revogacao")[0].classList.remove("hide");
      } else {
        document.getElementsByClassName("form-row field-documento_revogado")[0].classList.add("hide");
        document.getElementsByClassName("form-row field-tipo_revogacao")[0].classList.add("hide");
      }        
};

// Mostra/esconde div documentos se é um ato alterador
$(document).on("change", '#id_eh_alterador', function() {
    var remember = document.getElementById("id_eh_alterador");
    item = document.getElementsByClassName("form-row field-documento_alterado")[0]
    if (remember.checked) { 
        item.classList.remove("hide");
    } else {
        item.classList.add("hide");
    }        
});

// Mostra/esconde div documentos se é um ato revogador
$(document).on("change", '#id_eh_revogador', function() {
    var remember = document.getElementById("id_eh_revogador");
    documento_revogado = document.getElementsByClassName("form-row field-documento_revogado")[0]
    tipo_revogacao = document.getElementsByClassName("form-row field-tipo_revogacao")[0]
    if (remember.checked) {
        documento_revogado.classList.remove("hide");
        tipo_revogacao.classList.remove("hide");
      } else {
        documento_revogado.classList.add("hide");
        tipo_revogacao.classList.add("hide");
      }        
});

// Faz a requisição ajax para copular assuntos secundários conforme seleção de assunto principal
$(document).on("change", '#id_assuntos_from', function() {  
  console.log("Clique")
  var assuntos = $(this).val();
  console.log(assuntos)
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
        console.log(data);  
      }
    });
    $('select[name="assuntos_secundarios_old"]').prop("disabled", false);
  }
});