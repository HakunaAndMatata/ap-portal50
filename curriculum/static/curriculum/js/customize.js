$(document).ready(function() {
    $('#navbar-customize').addClass("active");
    $('#resource-table').DataTable({
                responsive: true,
                iDisplayLength: 10,
                language: {
                lengthMenu: 'Display <select class="form-control">'+
                    '<option value="5">5</option>'+
                    '<option value="10">10</option>'+
                    '<option value="15">15</option>'+
                    '<option value="-1">All</option>'+
                    '</select> resources',
                sInfo: "Showing _START_ to _END_ of _TOTAL_ resources",
                sEmptyTable: "There are no resources matching your query.",
                columns : [
                    null,
                    null,
                    { "width" : "50%" },
                    null,
                    null
                ]
            }
        });
    
    $('#cresource-table').DataTable({
                responsive: true,
                iDisplayLength: 10,
                language: {
                lengthMenu: 'Display <select class="form-control">'+
                    '<option value="5">5</option>'+
                    '<option value="10">10</option>'+
                    '<option value="15">15</option>'+
                    '<option value="-1">All</option>'+
                    '</select> resources',
                sInfo: "Showing _START_ to _END_ of _TOTAL_ resources",
                sEmptyTable: "There are no custom resources.",
                columns : [
                    null,
                    null,
                    { "width" : "50%" },
                    null,
                    null
                ]
            }
        });
    
     $('#sresource-table').DataTable({
                responsive: true,
                iDisplayLength: 10,
                language: {
                lengthMenu: 'Display <select class="form-control">'+
                    '<option value="5">5</option>'+
                    '<option value="10">10</option>'+
                    '<option value="15">15</option>'+
                    '<option value="-1">All</option>'+
                    '</select> resources',
                sInfo: "Showing _START_ to _END_ of _TOTAL_ resources",
                sEmptyTable: "There are no shared resources.",
                columns : [
                    null,
                    null,
                    { "width" : "50%" },
                    null,
                    null
                ]
            }
        });
    
    $('.btn-chapter-toggle').click(function() {
        toggleChapter($(this).data('chapter'));
    });
    
    $('.btn-module-toggle').click(function() {
       toggleModule($(this).data('module'), $(this).data('chapter'));
    });
    
    $('.btn-resource-toggle').click(function() {
       toggleResource($(this).data('resource'));
    });
    
    $('.btn-custom-save').click(function() {
        save();
    });
    
    $('.btn-add-resource').click(function() {
       addResource(); 
    });
    
    $('.show-edit-resource').click(function() {"
       showEditResource($(this).data('resource'));
    });

});
    
function toggleChapter(chapter_num) {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        chapter_num: chapter_num
    };
 
 var request = $.ajax({
    url: chapter_toggle_url,
    type: 'POST',
    data: parameters
 });
 
 request.done(function(response, textStatus, jqXHR) {
    data = jQuery.parseJSON(response);
    now_visible = data["new_val"];
     $('#c-vis-cell-' + chapter_num).html(now_visible ? "Yes" : "No");
 });
 request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
 });
}

    
function toggleModule(module_num, chapter_num) {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        module_num: module_num,
        chapter_num: chapter_num
    };
 
 var request = $.ajax({
    url: module_toggle_url,
    type: 'POST',
    data: parameters
 });
 
 request.done(function(response, textStatus, jqXHR) {
    data = jQuery.parseJSON(response);
    now_visible = data["new_val"];
     $('#m-vis-cell-' + module_num + '-' + chapter_num).html(now_visible ? "Yes" : "No");
 });
 request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
 });
}

function toggleResource(resource_id) {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        resource_id: resource_id
    };
 
 var request = $.ajax({
    url: resource_toggle_url,
    type: 'POST',
    data: parameters
 });
 
 request.done(function(response, textStatus, jqXHR) {
    data = jQuery.parseJSON(response);
    now_visible = data["new_val"];
     $('#r-vis-cell-' + resource_id).html(now_visible ? "Yes" : "No");
 });
 request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
 });
}

// save for the custom module information panel
function save() {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        module: modid,
        contents: $('#custom-area').val()
    };
    
    var request = $.ajax({
        url: update_modinfo_url,
        type: 'POST',
        data: parameters
    });
    
    request.done(function(response, textStatus, jqXHR) {
        $('#save-response').html('Saved successfully.')
    });
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
    });
}

function addResource() {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        module: modid,
        content: $('#add-resource-content').val(),
        link: $('#add-resource-link').val(),
        name: $('#add-resource-name').val(),
        rtype: $('#add-resource-rtype').val(),
        public: $('#add-resource-public').prop('checked')
    }
    
    var request = $.ajax({
        url: add_resource_url,
        type: 'POST',
        data: parameters
    });
    
    request.done(function(response, textStatus, jqXHR) {
        location.reload(true);
    });
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
    });
}

function showEditResource(id) {
    // get module to show up
    $("#edit-resource-modal").modal();
    // need to fill in the boxes with the right resource ID
    var parameters = {
        // only getting requests from sites authorizing
        csrfmiddlewaretoken: csrftoken,
        id: id
    };
    // make ajax request to curriculm/urls.py
    var request = $.ajax({
        url: access_resource_url,
        type: 'POST',
        data: parameters
    });
    
    // when request is done
    request.done(function(response, textStatus, jqXHR) {
        // turn string into json object
        data = jQuery.parseJSON(response);
        // load elements of text box
        $("#edit-resource-rtype").val(data["rtype"]);
        $("#edit-resource-name").val(data["name"]);
        $("#edit-resource-content").val(data["content"]);
        $("#edit-resource-link").val(data["link"]);
        console.log(data["shared"]);
        $("#edit-resource-public").prop('checked', data["shared"]);
        // makes a delete button
        var button = '<button onclick="showConfirmation('+id+')" type="button" class="btn btn-danger" data-dismiss="modal">Delete</button>';
        // add an edit button
        button += '<button onclick="editResource('+id+')" type="button" class="btn btn-primary">Save Changes</button>';
        $("#saveChangeArea").html(button);
        
    })
    
     request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
    });
}

function editResource(id) {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        id: id,
        content: $('#edit-resource-content').val(),
        link: $('#edit-resource-link').val(),
        name: $('#edit-resource-name').val(),
        rtype: $('#edit-resource-rtype').val(),
        public: $('#edit-resource-public').prop('checked')
    }
    
    var request = $.ajax({
        url: edit_resource_url,
        type: 'POST',
        data: parameters
    });
    
    request.done(function(response, textStatus, jqXHR) {
        location.reload(true);
    });
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
    });
}

function showConfirmation(id) {
    // get module to show up
    $("#delete-resource-modal").modal();
    // makes a delete button
    var button = '<button onclick="removeResource('+id+')" type="button" class="btn btn-danger">Delete</button>';
    $("#deleteConfirmation").html(button);
}
function removeResource(id) {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        id: id
    };
 
    var request = $.ajax({
    url: remove_resource_url,
    type: 'POST',
    data: parameters
    });
    
    request.done(function(response, textStatus, jqXHR) {
    location.reload(true);
    });
    
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
    });
}