var varTable;
$(document).ready(function () {
    $('.dropdown-search-filter').select2();
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable(0,0,0,0,0);
    loadClient();
    loadSection();
    //LoadCourseddl(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});
function loadSection(){
    var URL=$('#hdn_web_url').val()+ "/GetSectionCand"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Sections != null)
            {
                $('#ddlSection').empty();
                var count=data.Sections.length;
                if( count> 0)
                {
                    $('#ddlSection').append(new Option('Choose Section',''));
                    for(var i=0;i<count;i++)
                        $('#ddlSection').append(new Option(data.Sections[i].Section_Name,data.Sections[i].Section_Id));
                }
                else
                {
                    $('#ddlSection').append(new Option('Choose Section',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
}
function loadClient(){
    var URL=$('#hdn_web_url').val()+ "/GetALLClient"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Clients != null)
            {
                $('#ddlClient').empty();
                var count=data.Clients.length;
                if( count> 0)
                {
                    $('#ddlClient').append(new Option('Choose Customer',''));
                    for(var i=0;i<count;i++)
                        $('#ddlClient').append(new Option(data.Clients[i].Client_Name,data.Clients[i].Client_Id));
                }
                else
                {
                    $('#ddlClient').append(new Option('Choose Customer',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
}
function LoadProject(Client_id){
    var URL=$('#hdn_web_url').val()+ "/GetALLProject"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ClientId":Client_id
        },
        success: function (data){
            if(data.Projects != null)
            {
                $('#ddlProject').empty();
                var count=data.Projects.length;
                if( count> 0)
                {
                    $('#ddlProject').append(new Option('Choose Project',''));
                    for(var i=0;i<count;i++)
                        $('#ddlProject').append(new Option(data.Projects[i].Project_Name,data.Projects[i].Project_Id));
                }
                else
                {
                    $('#ddlProject').append(new Option('Choose Project',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadCourse(Project_Id){
    var URL=$('#hdn_web_url').val()+ "/get_cand_course_basedon_proj"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ProjectId":Project_Id
        },
        success: function (data){
            if(data.Courses != null)
            {
                $('#ddlCourse').empty();
                var count=data.Courses.length;
                if( count> 0)
                {
                    $('#ddlCourse').append(new Option('Choose Course',''));
                    for(var i=0;i<count;i++)
                        $('#ddlCourse').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                }
                else
                {
                    $('#ddlCourse').append(new Option('Choose Course',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadCenter(Course_Id){
    var URL=$('#hdn_web_url').val()+ "/get_cand_center_basedon_course"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "CourseId":Course_Id
        },
        success: function (data){
            if(data.Centers != null)
            {
                $('#ddlCenter').empty();
                var count=data.Centers.length;
                if( count> 0)
                {
                    $('#ddlCenter').append(new Option('Choose Center',''));
                    for(var i=0;i<count;i++)
                        $('#ddlCenter').append(new Option(data.Centers[i].Center_Name,data.Centers[i].Center_Id));
                }
                else
                {
                    $('#ddlCenter').append(new Option('Choose Center',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadTable(ClientId,ProjectId,CourseId,CenterId,SectionId)
{
    var course_id=CourseId
    var course_selected="",data='';
    var count;
    console.log(course_id.length);
    if (course_id == ""){
        course_selected='';
    }
    else{
        // count=course_id.length;
        // for (var i=0;i<count;i++){
        //     data+='{"course_id":'+ course_id[i]+'},';            
        // }
        // data=data.substring(0,data.length-1);
        // data='['+data+']';
        course_selected='[{"course_id":'+course_id+'}]';
    }
    console.log(course_selected);
    vartable1 = $("#tbl_candidate").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/candidate_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.candidate_id = 0;
                d.client_id =ClientId;
                d.project_id = ProjectId;
                d.course_id = course_selected;
                d.center_id =CenterId;
                d.section_id = SectionId;
				d.user_id = $('#hdn_home_user_id').val();
				d.user_role_id = $('#hdn_home_user_role_id').val();
				
            },
            error: function (e) {
                $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Candidate_Id"},
            { "data": "Candidate_Name"},
            { "data": "Mobile_Number"},
            { "data": "Course_Name"}
            // {
            // "data": function (row, type, val, meta) {
            // var varButtons = ""; 
            // if(role_id != 5)
            //     varButtons += '<a onclick="EditCenterTypeDetail(\'' + row.Candidate_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
            // return varButtons;
            // }
            // }
        ],


    });
}
function EditCandidateDetail(CandidateId)
{
    $('#hdn_candidate_id').val(CandidateId);
    $('#form1').submit();
    
}
function LoadCourseddl()
{
    //alert("course_section");
    var URL=$('#hdn_web_url').val()+ "/AllCourseList"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Courses != null)
            {
                $('#ddlCourse').empty();
                var count=data.Courses.length;
                if( count> 0)
                {
                    $('#ddlCourse').append(new Option('Choose Course','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCourse').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                }
                else
                {
                    $('#ddlCourse').append(new Option('Choose Course','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTableBasedOnSearch(){
    
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable($('#ddlClient').val(),$('#ddlProject').val(),$('#ddlCourse').val(),$('#ddlCenter').val(),$('#ddlSection').val()); 
}