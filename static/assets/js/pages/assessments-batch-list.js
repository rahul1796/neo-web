var varTable;
var varTable1;
var flag = "";
var role_id;

function LoadRegionddl(){
    var URL=$('#hdn_web_url').val()+ "/AllRegionsBasedOnUser"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id" : $('#hdn_home_user_role_id').val(),
            "user_region_id" : $('#hdn_user_region_id').val()
        },

        success: function (data){
            if(data.Regions != null)
            {
                $('#ddlRegion').empty();
                var count=data.Regions.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRegion').append(new Option(data.Regions[i].Region_Name,data.Regions[i].Region_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlRegion').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading BU! Please try again');
            return false;
        }
    });
    return false;
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
                    //$('#ddlClient').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlClient').append(new Option(data.Clients[i].Customer_Name,data.Clients[i].Customer_Id));
                }
                else
                {
                    $('#ddlClient').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            //alert($('#ddlClient').val().toString())
            alert('Error! Please try again');
            return false;
        }
    });
}

function LoadProject(){
    var URL=$('#hdn_web_url').val()+ "/GetALLProject_multiple"  //"/GetALLProject_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ClientId":$('#ddlClient').val().toString()
        },
        success: function (data){
            if(data.Projects != null)
            {
                $('#ddlProject').empty();
                var count=data.Projects.length;
                if( count> 0)
                {
                    //$('#ddlProject').append(new Option('ALL','-1'));  , 
                    for(var i=0;i<count;i++)
                        $('#ddlProject').append(new Option(data.Projects[i].Project_Name,data.Projects[i].Project_Id));
                }
                else
                {
                    $('#ddlProject').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(request, err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadSubProject(){
    //alert($('#ddlProject').val().toString())
    var URL=$('#hdn_web_url').val()+ "/get_subproject_basedon_proj_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ProjectId":$('#ddlProject').val().toString()
        },
        success: function (data){
            if(data.Sub_Project != null)
            {
                $('#ddlSubProject').empty();
                var count=data.Sub_Project.length;
                if( count> 0)
                {
                    //$('#ddlCourse').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlSubProject').append(new Option(data.Sub_Project[i].Sub_Project_Name,data.Sub_Project[i].Sub_Project_Id));
                }
                else
                {
                    $('#ddlSubProject').append(new Option('ALL','-1'));
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

function LoadCenter(){
    var URL=$('#hdn_web_url').val()+ "/get_cand_center_basedon_course_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "CourseId":"",
            "RegionId":$('#ddlRegion').val().toString()
        },
        success: function (data){
            if(data.Centers != null)
            {
                $('#ddlCenter').empty();
                var count=data.Centers.length;
                if( count> 0)
                {
                    //$('#ddlCenter').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCenter').append(new Option(data.Centers[i].Center_Name,data.Centers[i].Center_Id));
                }
                else
                {
                    $('#ddlCenter').append(new Option('ALL','-1'));
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
function LoadTable()
{   
    $('#divBcthList').show();
    vartable = $("#tbl_batchs").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": true,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/batch_list_updated",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.batch_id = 0;
		        d.user_id = $('#hdn_home_user_id').val();
                d.user_role_id  = $('#hdn_home_user_role_id').val();
                d.status = '';
                d.customer = $('#ddlClient').val().toString();
                d.project = $('#ddlProject').val().toString();
                d.sub_project = $('#ddlSubProject').val().toString();
                d.region = $('#ddlRegion').val().toString();
                d.center = $('#ddlCenter').val().toString();
                d.center_type = $('#ddlCenterType').val().toString();
                d.course_ids= $('#ddlCourse').val().toString();
            },
            error: function (e) {
                $("#tbl_batchs tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [

            								
            { "data": "S_No"},
            { "orderable":false,
                "data": function(row, type, val, meta) {
                    var varButtons='';
                    varButtons+='<a onclick="ScheduleAssessmentModal(\'' + row.Batch_Id + '\',\'' + row.Batch_Code + '\')" class="btn" style="cursor:pointer" ><i title="Schedule Assessment" class="fe-edit" ></i></a>';
                    varButtons+='<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + row.Batch_Code + '\')" class="btn" style="cursor:pointer" ><i title="Assessment List" class="fas fa-list" ></i></a>';
                    return varButtons;
                }
            },            
            { "data": "Batch_Name" },
            { "data": "Batch_Code"},
            { "data": "Product_Name" },
            {
                "data": function (row, type, val, meta) {
                    /*var varButtons = ""; 
                    if(row.Center_Name=="")
                    {
                        varButtons=row.Center_Name;
                    }                        
                    else
                    {   
                        varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id + '\',\'' + row.Center_Name + '\' )"  style="color:blue;cursor:pointer" >' + row.Center_Name + '</a>';
                    }
                    
                    return varButtons;
                */
                    return row.Center_Name;    
                }                    
            },
            {
                "data": function (row, type, val, meta) {
                    /*var varButtons = "";
                    if(row.Course_Name=="")
                        {
                            varButtons=row.Course_Name;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetCourseDetail(\'' + row.Course_Id +  '\' )"  style="color:blue;cursor:pointer" >' + row.Course_Name + '</a>';
                    }
                    
                    return varButtons;*/
                    return row.Course_Name;
                    }
            },
            { "data": "Sub_Project_Name" },
            {
                "data": function (row, type, val, meta) {
                    /*var varButtons = ""; 
                    if(row.Trainer_Email=="")
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Trainer_Email;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetUserDetail(\'' + row.Trainer_Id + '\',\'' + 'trainer' + '\' )"  style="color:blue;cursor:pointer" >' + row.Trainer_Email + '</a>';
                    }
                    */
                    return row.Trainer_Email;
                    }
            },
            //{ "data": "Trainer_Email" },
            { "data": "Center_Manager_Email" },
            { "data": "Start_Date" },
            { "data": "End_Date" },
            { "data": "Start_Time"},
            { "data": "End_Time"},
            { "data": "Status"}
        ],
        drawCallback: function(){
            $('#tbl_batchs_paginate ul.pagination').addClass("pagination-rounded");
        }
    });
}
function EditBatchDetail(BatchId)
{
    $('#hdn_batch_id').val(BatchId);
    $('#form1').submit();
    
}


function MapCandidateBatch(CourseId,CenterId,BatchId){
                flag='map'
                $('#tbl_candidate').show();
                $('#tbl_drop_candidate').hide();
                $('#tbl_drop_candidate').dataTable().fnDestroy();
                $('#tbl_candidate').dataTable().fnDestroy();

                //alert(CourseId + ',' + CenterId + ',' + BatchId)
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
                    "url": $('#hdn_web_url').val()+ "/ALLCandidatesBasedOnCourse",
                    "type": "POST",
                    "dataType": "json",
                    "data": function (d) {
                        d.candidate_id = 0;
                        d.course_id = CourseId;
                        d.center_id = CenterId;
                        d.batch_id = BatchId;
                    },
                    error: function (e) {
                        $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
                    }

                },

                "columns": [
                    { "data": "S_No"},
                    {
                        "data": function (row, type, val, meta) {
                        if(row.Is_Added){
                            var varButtons = "";
                                varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" checked>';
                            return varButtons;
                        }
                        else{
                            var varButtons = "";
                                varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" >';
                            return varButtons;
                        }
                        }
                    },
                    { "data": "Candidate_Id"},
                    { "data": "Candidate_Name" },
                    { "data": "Course_Name" },
                    { "data": "Center_Name"},
                    { "data": "Mobile_Number" },
                    { "data": "Registration_Id" },
                    { "data": "Enrollment_Id" },
                    { "data": "Salutaion"}
                    
                ],
            });
            // if(addch){
            //     $('#addedchk').prop('checked',true);
            // }
            // else{
            //     $('#addedchk').prop('checked',false);
            // }
            Course=CourseId;
            Batch=BatchId;
            $('#get0').hide();
            $('#get').hide();
            $('.center').show();
            

}

function DropCandidateBatch(CourseId,CenterId,BatchId){
    flag='drop'
    $('#tbl_candidate').hide();
    $('#tbl_drop_candidate').show();
    $('#tbl_candidate').dataTable().fnDestroy();
    $('#tbl_drop_candidate').dataTable().fnDestroy();



    vartable2 = $("#tbl_drop_candidate").DataTable({
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
        "url": $('#hdn_web_url').val()+ "/ALLCandidatesMapedInBatch",
        "type": "POST",
        "dataType": "json",
        "data": function (d) {
            d.candidate_id = 0;
            d.course_id = CourseId;
            d.center_id = CenterId;
            d.batch_id = BatchId;
        },
        error: function (e) {
            $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
        }

    },

    "columns": [
        { "data": "S_No"},
        {
            "data": function (row, type, val, meta) {
            if(row.Is_Added){
                var varButtons = "";
                    varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" checked>';
                return varButtons;
            }
            else{
                var varButtons = "";
                    varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" >';
                return varButtons;
            }
            }
        },
        { "data": "Candidate_Id"},
        { "data": "Candidate_Name" },
        { "data": "Course_Name" },
        { "data": "Center_Name"},
        { "data": "Mobile_Number" },
        { "data": "Registration_Id" },
        { "data": "Enrollment_Id" },
        { "data": "Salutaion"}
        
    ],
});
// if(addch){
//     $('#addedchk').prop('checked',true);
// }
// else{
//     $('#addedchk').prop('checked',false);
// }
Course=CourseId;
Batch=BatchId;
$('#get').hide();
$('#get0').hide();
$('.center').show();

}
function save(){
    if(flag == 'drop' ){
        if($('#txtremark').val()!=''){
            add_drop_message();
        }
        else{
            $('#con_close_modal').modal('show');
        }
        
    }
    else if(flag=='map'){
        //alert(flag)
        add_map_message();
    }
}
function add_map_message(){
    var cands='';
    //alert(flag)
    $('[name=checkcase]:checked').each(function () {
        cands+= $(this).val()+',';
    });
    cands=cands.substring(0,cands.length-1)
    var URL=$('#hdn_web_url').val()+ "/add_edit_map_candidate_batch";
        //alert($('#ddlCourse').val());
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "course_id": Course,
                    "candidate_ids": cands.toString(),
                    "batch_id": Batch
                },
                success:function(data){
                    // var table = $('#tbl_candidate');
                    
                    // swal({
                    //     html: table
                    // }).then(function(){
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" Done Successfully !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/after_popup_batch';
                        });
                //    alert("The Inserted/Upadated Id is "+data.PopupMessage.message);
                //    window.location.href="/after_popup"; 
                // })
                },
                error:function(err)
                {
                    alert('Error! Please try again');
                    return false;
                }
            });
    }
    function add_drop_message(){
        
        var cands='';
        //alert(flag)
        $('[name=checkcase]:checked').each(function () {
            cands+= $(this).val()+',';
        });
        cands=cands.substring(0,cands.length-1)
	
        var URL=$('#hdn_web_url').val()+ "/drop_edit_candidate_batch";
        //alert(Course + ',' + Batch +',' + $('#txtremark').val())
            //alert($('#ddlCourse').val());
                $.ajax({
                    type:"POST",
                    url:URL,
                    data:{
                        "course_id": Course,
                        "candidate_ids": cands.toString(),
                        "batch_id": Batch,
                        "drop_remark": $('#txtremark').val()
                    },
                    success:function(data){
                        // var table = $('#tbl_candidate');
                        
                        // swal({
                        //     html: table
                        // }).then(function(){
                        swal({   
                            title:data.PopupMessage.message,
                            text:data.PopupMessage.message+" Done Successfully !!",
                            icon:"success",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/after_popup_batch';
                            });
                    //    alert("The Inserted/Upadated Id is "+data.PopupMessage.message);
                    //    window.location.href="/after_popup"; 
                    // })
                    },
                    error:function(err)
                    {
                        alert('Error! Please try again');
                        return false;
                    }
                });
        }

    function GetProjectDetails(CenterId,CenterName)
    {
        var URL=$('#hdn_web_url').val()+ "/GetSubProjectsForCenter?center_id="+CenterId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                $("#tblSubProject tbody").empty();
                if(!jQuery.isEmptyObject(data.SubProjects))
                {   if (data.SubProjects != null){
                        count=data.SubProjects.length;
                        if (count>0)
                        {   varHtml='';
                            console.log(count);
                            for(var i=0;i<count;i++)
                            {
                                td_open= '  <td style="text-align:center;">' ;
                                td_close=   '</td>';       
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].S_No +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ CenterName +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Sub_Project_Code +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Sub_Project_Name +'</td>';                    
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Project_Code +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Project_Name +'</td>';  
                                varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Bu +'</td>';         
                                varHtml+='</tr>';
                                $("#tblSubProject tbody").append(varHtml);
                                $('#divSubProjectList').modal('show');
                                varHtml='';
                            }
                        }
                        else
                        {
                            varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                            $("#tblSubProject tbody").append(varHtml);
                            $('#divSubProjectList').modal('show');
                        } 
                        
                    }
                }
                else
                {
                    varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                    $("#tblSubProject tbody").append(varHtml);
                    $('#divSubProjectList').modal('show');
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

    function LoadCenterType()
    {       
        var URL=$('#hdn_web_url').val()+ "/AllCenterTypes"
        $.ajax({
            type:"GET",
            url:URL,
            async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            data:{
                    "user_id": $('#hdn_home_user_id').val(),
                    "user_role_id" : $('#hdn_home_user_role_id').val()
            },
            success: function (data){
                if(data.Center_Types != null)
                {
                    $('#ddlCenterType').empty();
                    var count=data.Center_Types.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            $('#ddlCenterType').append(new Option(data.Center_Types[i].Center_Type_Name,data.Center_Types[i].Center_Type_Id));                    
                    }
                    else
                    {
                        $('#ddlCenterType').append(new Option('ALL',''));
                    }
                    $("#ddlCenterType option[value='']").attr('disabled','disabled');
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

    function GetUserDetail(user_id,type)
    {
        var URL=$('#hdn_web_url').val()+ "/get_user_details_new?user_id="+user_id;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){

                $('#txtEmployee_Code').val(data.UserDetail.Employee_Code);
                $('#txtname').val(data.UserDetail.Name);
                $('#txtEmail').val(data.UserDetail.Email);
                $('#txtMobile_Number').val(data.UserDetail.Mobile_Number);
                $('#txtEmployment_Grade').val(data.UserDetail.Employment_Grade_Id);
                $('#txtEmployment_Status').val(data.UserDetail.Employment_Status_Id);
                $('#txtReporting_Manager_Name').val(data.UserDetail.Reporting_Manager_Name);
                $('#txtEmployee_Department_Name').val(data.UserDetail.Employee_Department_Name);
                $('#txtEntity_Name').val(data.UserDetail.Entity_Name);

                $('#trainer_details_modal').modal('show');
                        
            },
            error:function(err)
            {
                alert('Error! Please try again');
                return false;
            }
        });
        return false;
    }

    function GetCourseDetail(course_id)
    {
        var URL=$('#hdn_web_url').val()+ "/GetCourseDetails?course_id="+course_id;
        
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                
                $('#txtSub_Project_Name').val(data.CourseDetail.Sub_Project_Name);
                $('#txtCourse_Code').val(data.CourseDetail.Course_Code);
                $('#txtCourse_Name').val(data.CourseDetail.Course_Name);
                
                $('#course_details_modal').modal('show');
                        
            },
            error:function(err)
            {
                alert('Error! Please try again');
                return false;
            }
        });
        return false;
    }

    function GetAssessments(BatchId,BatchCode){
        var URL=$('#hdn_web_url').val()+ "/GetBatchAssessments?BatchId="+BatchId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                let varTxt='';
                $("#tbl_batch_assessment tbody").empty();
                if(!jQuery.isEmptyObject(data))
                {   
                    if (data.Assessments != null){
                        var count=data.Assessments.length;
                        if( count> 0)
                        {
                            for(var i=0;i<count;i++)
                            {   var txt=''
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].S_No +'</td>';
                                txt='<a onclick="DownloadAssessmentResult(\'' + data.Assessments[i].Assessment_Id + '\')" class="btn" style="cursor:pointer" ><i title="Download Assessment Result" class="fe-download" ></i></a>';
                                txt+='<a onclick="EditAssessmentDetails(\'' + data.Assessments[i].Assessment_Id + '\',\'' + data.Assessments[i].Requested_Date + '\',\'' + data.Assessments[i].Scheduled_Date + '\',\'' + data.Assessments[i].Assessment_Types_Id + '\',\'' + data.Assessments[i].Assessment_Agency_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Assessment Detail" class="fe-edit-1" ></i></a>';
                                varHtml+='  <td style="text-align:center;">'+ txt +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Batch_Code +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_On +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Scheduled_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Types_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Agency_Name +'</td>';
                                varHtml+='</tr>';

                            }                        
                        }
                        $("#tbl_batch_assessment tbody").append(varHtml);
                        $('#mdl_batch_assessments').modal('show');
                    }
                    else
                    {
                        varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_batch_assessment tbody").append(varHtml);
                        $('#mdl_batch_assessments').modal('show');
                    }
                }
                else
                {
                    varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_batch_assessment tbody").append(varHtml);
                    $('#mdl_batch_assessments').modal('show');
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
    function ScheduleAssessmentModal(BatchId,BatchCode){
        LoadAssessmentTypes();
        LoadAssessmentAgency();
        $('#TxtRequestedDate').val('');
        $('#TxtScheduledDate').val('');
        $('#hdn_batch_assessment_id').val(BatchId);
        $('#mdl_create_batch_assessments').modal('show');
    }
    function EditAssessmentDetails(AssessmentId,ReqDate,SchDate,AssessmentTypeId,AssessmentAgencyId)
    {
        LoadAssessmentTypes();
        LoadAssessmentAgency();
        $('#TxtRequestedDate').val(ReqDate);
        $('#TxtScheduledDate').val(SchDate);
        $('#ddlAssessmentType').val(AssessmentTypeId);
        $('#ddlAssessmentAgency').val(AssessmentAgencyId);
        $('#hdn_assessment_id').val(AssessmentId);
        $('#mdl_batch_assessments').modal('hide');
        $('#mdl_create_batch_assessments').modal('show');
    }
    function LoadAssessmentTypes(){
        var URL=$('#hdn_web_url').val()+ "/GetAssessmentTypes"
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                if(data.AssessmentTypes != null)
                {
                    $('#ddlAssessmentType').empty();
                    var count=data.AssessmentTypes.length;
                    $('#ddlAssessmentType').append(new Option('Select',''));
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            $('#ddlAssessmentType').append(new Option(data.AssessmentTypes[i].Assessment_Types_Name,data.AssessmentTypes[i].Assessment_Types_Id));
                    }
                    else
                    {
                        $('#ddlAssessmentType').append(new Option('ALL','-1'));
                    }
                }
            },
            error:function(err)
            {
                alert('Error loading assessment types! Please try again');
                return false;
            }
        });
    }
    function LoadAssessmentAgency(){
        var URL=$('#hdn_web_url').val()+ "/GetAssessmentAgency"
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                if(data.AssessmentAgency != null)
                {
                    $('#ddlAssessmentAgency').empty();
                    var count=data.AssessmentAgency.length;
                    $('#ddlAssessmentAgency').append(new Option('Select',''));
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            $('#ddlAssessmentAgency').append(new Option(data.AssessmentAgency[i].Assessment_Agency_Name,data.AssessmentAgency[i].Assessment_Agency_Id));
                    }
                    else
                    {
                        $('#ddlAssessmentAgency').append(new Option('ALL','-1'));
                    }
                }
            },
            error:function(err)
            {
                alert('Error loading assessment types! Please try again');
                return false;
            }
        });
    }
    function ScheduleAssessment()
    {   
        if($('#TxtRequestedDate').val()=='')
            alert("Please enter requested date.");
        console.log($('#hdn_batch_assessment_id').val(),$('#ddlAssessmentType').val(),$('#TxtRequestedDate').val(),$('#TxtScheduledDate').val(),$('#ddlAssessmentAgency').val());
        var URL=$('#hdn_web_url').val()+ "/ScheduleAssessment";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "batch_id" : $('#hdn_batch_assessment_id').val(),
                    "user_id" : $('#hdn_home_user_id').val(),
                    "requested_date" : $('#TxtRequestedDate').val(),
                    "scheduled_date" : $('#TxtScheduledDate').val(),
                    "assessment_agency_id" : $('#ddlAssessmentAgency').val(),
                    "assessment_type_id" : $('#ddlAssessmentType').val(),
                    "assessment_id" : $('#hdn_assessment_id').val()
                },
                success:function(data){
                    var message="",title="",icon="";
                    if(data.success==0){
                        message=data.message;
                        title="Error";
                        icon="error";
                    }
                    else{
                        message=data.message;
                        title="Success";
                        icon="success";
                    }
                    swal({   
                                title:title,
                                text:message,
                                icon:icon,
                                confirmButtonClass:"btn btn-confirm mt-2"
                                }).then(function(){
                                    LoadTable();
                                    $('#mdl_create_batch_assessments').modal('hide');
                                }); 
                },
                error:function(x){
                    alert('error');
                }
            });
    
    }

    function DownloadAssessmentResult(AssessmentId)
    {         
        //$('#divLoader').show();        
        var URL=$('#hdn_web_url').val()+ "/DownloadAssessmentResult?AssessmentId="+AssessmentId;            
        $.ajax({
            type:"GET",
            url:URL,
            async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            data:{       
            },
            success:function(data){
                if(data!=null)
                {                       
                    window.location=data.FilePath+data.FileName;
                    //$('#divLoader').hide();
                }                    
            },
            error:function(x){
                alert('Error while downloading Report. ');
            }
        });        
    }