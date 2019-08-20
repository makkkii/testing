function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    // var formIndex = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    // console.log(prefix, btn)
    var formIndex = parseInt($('[data-form-list="'+ prefix + '-prefix"] .dynamic-form:last').prop("id").match(/\d+-row/)[0].split("-")[0])+1;

    // console.log(12)
    // console.log(prefix, formIndex, $("#id_"+prefix+"-MAX_NUM_FORMS").val())
    if ($('[data-form-list="'+ prefix + '-prefix"] .dynamic-form').length >= $("#id_"+prefix+"-MAX_NUM_FORMS").val()){
        return false;
    }
    if ( typeof before_clone == 'function' ) {
        before_clone();
    }

    // console.log('[data-form-list="'+ prefix + '-prefix"] .dynamic-form:first');

    var row = $('[data-form-list="'+ prefix + '-prefix"] .dynamic-form:first').clone(true).get(0);
    $.each($(row).find(":input"), function(i,v){
        $(v).prop("name",$(v).prop("name").replace("-0-", "-"+formIndex+"-"));
        $(v).prop("id",$(v).prop("id").replace("-0-", "-"+formIndex+"-"));
        $(v).val("")
    });

    $.each($(row).find("label"), function(i,v){
        $(v).prop("for", $(v).prop("for").replace("-0-", "-"+formIndex+"-"));
    });

    $(row).prop("id", $(row).prop("id").replace("-0-", "-"+formIndex+"-"));
    $(row).find('div.d-none').remove();
    $(row).insertAfter($('[data-form-list="'+ prefix + '-prefix"] .dynamic-form:last')).find('.d-none').removeClass('d-none');

    $('[data-form-list="'+ prefix + '-prefix"] .dynamic-form .add-row').not(':first').remove();
    $(row).find("ul.errorlist").remove();
    $(row).children().not(':last').children().each(function () {
        updateElementIndex(this, prefix, formIndex);
    });

    $(row).find('.delete-row').click(function () {
        deleteForm(this, prefix);
    });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formIndex + 1);

    if (typeof after_clone == 'function') {
        after_clone();
    }
    // if ( typeof dynamic_refresh == 'function' ) {
    //     dynamic_refresh();
    // }
    return false;
}

function deleteForm(btn, prefix) {
    // console.log($(btn).parents('.dynamic-form').html())
    if($(btn).parents('.dynamic-form').find('input[type="hidden"][name*="-id"]').val()==""){
        $(btn).parents('.dynamic-form').remove();
    }else {
        $(btn).parents('.dynamic-form').hide();
        $(btn).parents('.dynamic-form').find('input[type="checkbox"][name*="-DELETE"]').prop("checked", true)
    }
    var forms = $('[data-form-list="'+ prefix + '-prefix"] .dynamic-form');

    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).children().not(':last').children().each(function () {
            updateElementIndex(this, prefix, i);
        });
    }
    return false;
}

$(function () {
    $('[data-form-list*="prefix"] .add-row').click(function() {
        return addForm(this, $(this).data('prefix'));
    });
    $('[data-form-list*="prefix"] .delete-row').click(function() {
        return deleteForm(this, $(this).data('prefix'));
    });
    $.each($('input[type="checkbox"][name*="-DELETE"][id*="-DELETE"]'), function (i, v) {
        $(v).hide();
        if($(v).is(":checked")){
            //In case a form was submited and filed (so we want to represent the form for corrections) Hide already deleted
            $(v).parents('.dynamic-form').hide();
        }
    });
});



//******************************** :New Start: *********************************//
$('#add_more').click(function() {
    cloneMore('div.table:last', 'service');
});

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}