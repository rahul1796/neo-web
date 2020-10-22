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
function LoadAssessmentStages(){
    var URL=$('#hdn_web_url').val()+ "/AllAssessmentStages"
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
            if(data.AssessmentStages != null)
            {
                $('#ddlAssessmentStages').empty();
                $('#ddlAssessmentStages').append(new Option('ALL Stages','0'));
                var count=data.AssessmentStages.length;
                if( count> 0)
                {
                  
                   for(var i=0;i<count;i++)
                        $('#ddlAssessmentStages').append(new Option(data.AssessmentStages[i].Assessment_Stage_Name,data.AssessmentStages[i].Assessment_Stage_Id));
                }
                else
                {
                    $('#ddlAssessmentStages').append(new Option('ALL',''));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Assessment Stages! Please try again');
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
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
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
            "ClientId":$('#ddlClient').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
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
            "ProjectId":$('#ddlProject').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
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
    var URL=$('#hdn_web_url').val()+ "/GetAllCentersBasedOnRegion_User"
    $.ajax({
        type:"Get",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            //"CourseId":"",
            "region_id":$('#ddlRegion').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
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
                   // $('#ddlCenter').append(new Option('ALL','-1'));
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
            "url": $('#hdn_web_url').val()+ "/batch_list_assessment",
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
                d.assessment_stage_id= $('#ddlAssessmentStages').val().toString();
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
                    if($('#hdn_home_user_role_id').val()!='25' & $('#hdn_home_user_role_id').val()!='28'  & row.Summative_Count==0)
                    {
                        if($('#hdn_home_user_role_id').val()!='37')
                            varButtons+='<a onclick="ScheduleAssessmentModal(\'' + row.Batch_Id + '\',\'' + row.Batch_Code + '\',\'' + row.Mobilization_Type + '\')" class="btn" style="cursor:pointer" ><i title="Schedule Assessment" class="fe-edit" ></i></a>';
                    
                    }
                        //varButtons+='<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + row.Batch_Code + '\')" class="btn" style="cursor:pointer" ><i title="Assessment List" class="fas fa-list" ></i></a>';
                    return varButtons;
                }
            },            
            
            {
                "data": function (row, type, val, meta) {
                    var varButtons = "";
                    if(row.Batch_Code=="")
                        {
                            varButtons=row.Batch_Code;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetBatchDetails(\'' + row.Batch_Code +  '\' )"  style="color:blue;cursor:pointer" >' + row.Batch_Code + '</a>';
                    }
                    
                    return varButtons;
                    return row.Batch_Code;
                    }
            },
            { "data": "Status"},
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Proposed==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Proposed;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + 1 + '\' )"  style="color:blue;cursor:pointer" >' + row.Proposed + '</a>';
                    }
                    return varButtons;
                    return row.proposed;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Confirmed==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Confirmed;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + 2 + '\' )"  style="color:blue;cursor:pointer" >' + row.Confirmed + '</a>';
                    }
                    return varButtons;
                    return row.Confirmed;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Assessed==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Assessed;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + 3 + '\' )"  style="color:blue;cursor:pointer" >' + row.Assessed + '</a>';
                    }
                    return varButtons;
                    return row.Assessed;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Result_Uploaded==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Result_Uploaded;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetAssessments(\'' + row.Batch_Id + '\',\'' + 4 + '\' )"  style="color:blue;cursor:pointer" >' + row.Result_Uploaded + '</a>';
                    }
                    return varButtons;
                    return row.Result_Uploaded;
                    }
            }

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
function GetBatchDetails(BatchCode)
    {
        var URL=$('#hdn_web_url').val()+ "/GetBatchDetailsAssessment?batch_code="+BatchCode;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                $("#tblBatchDetails tbody").empty();
                if(!jQuery.isEmptyObject(data.Batches))
                {   if (data.Batches != null){
                        count=data.Batches.length;
                        if (count>0)
                        {   varHtml='';
                            //console.log(count);
                            for(var i=0;i<count;i++)
                            {
                                td_open= '  <td style="text-align:center;">' ;
                                td_close=   '</td>';       
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].S_No +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ BatchCode +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Batch_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Candidate_Count +'</td>';                    
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Center_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Course_Name +'</td>';  
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Sub_Project_Name +'</td>'; 
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Trainer_Email +'</td>'; 
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].Start_Date +'</td>'; 
                                varHtml+='  <td style="text-align:center;">'+ data.Batches[i].End_Date +'</td>';         
                                varHtml+='</tr>';
                                $("#tblBatchDetails tbody").append(varHtml);
                                $('#divBatchDetails').modal('show');
                                varHtml='';
                            }
                        }
                        else
                        {
                            varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                            $("#tblBatchDetails tbody").append(varHtml);
                            $('#divBatchDetails').modal('show');
                        } 
                        
                    }
                }
                else
                {
                    varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                    $("#tblBatchDetails tbody").append(varHtml);
                    $('#divBatchDetails').modal('show');
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
function toggleCheckbox(e)
{
    var temp=e.target.getAttribute('value');
    if($('#'+e.target.getAttribute('id')).is(':checked'))
    {
        $('[name=checkcase]').each(function () {
                $(this).prop("checked", true);
        });
    }
    else
    {
        $('[name=checkcase]').each(function () {
            $(this).prop("checked", false);
        });
    }
    //console.log(check_list)
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

    function GetAssessments(BatchId,Stage){
        $('#hdn_batch_assessment_id').val(BatchId);
        var URL=$('#hdn_web_url').val()+ "/GetBatchAssessments?BatchId="+BatchId+"&Stage="+Stage;
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
                                var attempt=''
                                if(!($("#hdn_home_user_role_id ").val() == "25"  & data.Assessments[i].Assessment_Agency_Id==1))
                                {
                                    varHtml+='<tr>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].S_No +'</td>';
                                    if(data.Assessments[i].Assessment_Stage_Id==4) // Assessment Result Uploaded
                                        txt+='<a onclick="DownloadAssessmentResult(\'' + data.Assessments[i].Assessment_Id + '\',\'' + data.Assessments[i].Batch_Code + '\')" class="user-btn" style="cursor:pointer" ><i title="Download Assessment Result" class="fe-download" ></i></a>';
                                    if (data.Assessments[i].Assessment_Stage_Id<3 && (data.Assessments[i].Mobilization_Type!=4)  )
                                    {
                                        if( !(($("#hdn_home_user_role_id ").val() == "7" || $("#hdn_home_user_role_id ").val() == "5"||$("#hdn_home_user_role_id ").val() == "38"|| $("#hdn_home_user_role_id ").val() == "14") & (data.Assessments[i].Assessment_Types_Name=="Final Summative" || data.Assessments[i].Assessment_Types_Name=="Summative" )))  
                                            txt+='<a onclick="EditAssessmentDetails(\'' + data.Assessments[i].Assessment_Id + '\',\''+ data.Assessments[i].Partner_Category_Id +'\',\'' + data.Assessments[i].Requested_Date + '\',\'' + data.Assessments[i].Scheduled_Date + '\',\'' + data.Assessments[i].Assessment_Types_Id + '\',\'' + data.Assessments[i].Assessment_Agency_Id + '\',\'' + data.Assessments[i].Assessment_Stage_Id + '\',\'' + data.Assessments[i].Partner_Id + '\',\'' + data.Assessments[i].Assessment_Date + '\')" class="user-btn" style="cursor:pointer" ><i title="Edit Assessment Detail" class="fe-edit-1" ></i></a>';
                                    }
                                    if ((data.Assessments[i].Mobilization_Type==4 & ($("#hdn_home_user_role_id ").val() == "5" ||$("#hdn_home_user_role_id ").val() == "38" || $("#hdn_home_user_role_id ").val() == "1" ))||(data.Assessments[i].Assessment_Stage_Id==3 & (data.Assessments[i].Assessment_Agency_Id==1 & ($('#hdn_home_user_role_id').val()=='5'||$('#hdn_home_user_role_id').val()=='38') ) & $('#hdn_home_user_role_id').val()!='14'))
                                    {
                                        if( !($("#hdn_home_user_role_id ").val() == "7"  & (data.Assessments[i].Assessment_Types_Name=="Final Summative" || data.Assessments[i].Assessment_Types_Name=="Summative") ))
                                            txt+='<a onclick="UploadResult(\'' + data.Assessments[i].Assessment_Id + '\',\'' + data.Assessments[i].Batch_Id + '\',\'' + data.Assessments[i].Assessment_Stage_Id + '\',\'' + data.Assessments[i].Batch_Code + '\',\'' + data.Assessments[i].Requested_Date + '\',\'' + data.Assessments[i].Scheduled_Date + '\',\'' + data.Assessments[i].Assessment_Date + '\')" class="user-btn" style="cursor:pointer" ><i title="Upload Result" class="fe-upload" ></i></a>';
                                    }                                     
                                    if ((data.Assessments[i].Assessment_Stage_Id>=3 & $('#hdn_home_user_role_id').val()!='25')  )
                                        txt+='<a onclick="Reassessment(\'' + data.Assessments[i].Assessment_Id + '\',\''+ data.Assessments[i].Batch_Id +'\',\''+ data.Assessments[i].Partner_Category_Id +'\',\'' + data.Assessments[i].Requested_Date + '\',\'' + data.Assessments[i].Scheduled_Date + '\',\'' + data.Assessments[i].Assessment_Types_Id + '\',\'' + data.Assessments[i].Assessment_Agency_Id + '\',\'' + data.Assessments[i].Assessment_Stage_Id + '\',\'' + data.Assessments[i].Partner_Id + '\',\'' + data.Assessments[i].Assessment_Date + '\')" class="user-btn" style="cursor:pointer" ><i title="Schedule Reassessment" class="fe-edit" ></i></a>';
                                    if($('#hdn_home_user_role_id').val()!='37' & $('#hdn_home_user_role_id').val()!='28')
                                        varHtml+='  <td style="text-align:center;">'+ txt +'</td>';
                                    else
                                        varHtml+='  <td style="text-align:center;">'+ ''+'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Batch_Code +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_Date +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_On +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Scheduled_Date +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Date +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Types_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Agency_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Partner_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Stage_Name +'</td>';
                                    if(data.Assessments[i].Attempt >1)
                                        attempt+=  '<a onclick="AssessmentListHistory(\'' + data.Assessments[i].Assessment_Id + '\')" style="color:blue;cursor:pointer" >'+data.Assessments[i].Attempt+'</a>';
                                    else
                                        attempt+= data.Assessments[i].Attempt
                                    varHtml+='  <td style="text-align:center;">'+ attempt +'</td>';
                                    varHtml+='</tr>';
                                }
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
    function ScheduleAssessmentModal(BatchId,BatchCode,Mobilization_Type){
        LoadAssessmentTypes();
        LoadAssessmentAgency();
        $('#TxtRequestedDate').val('');
        $('#DivScheduleDate').hide();
        $('#DivAssessmentDate').hide();
        $('#DivAssessorName').hide();
        $('#DivAssessorMob').hide();
        $('#DivAssessorEmail').hide();
        $('#DivCandidates').show();
        AbsentCandidateBatch(BatchId,0,0);  
        $('#TxtScheduledDate').val('');
        $('#TxtAssessmnetDate').val('');
        $('#hdnMobilizationType').val(Mobilization_Type);
        $('#hdn_batch_assessment_id').val(BatchId);
        $('#ddlAssessmentType').attr('disabled', false);
        $('#ddlAssessmentAgency').attr('disabled', false);
        $('#ddlPartner').attr('disabled', false);
        $('#TxtRequestedDate').attr('disabled', false);
        $('#mdl_create_batch_assessments').modal('show');
    }
    function ScheduleReAssessmentModal(AssessmentId,BatchId,Partner_Category_Id,ReqDate,SchDate,AssessmentTypeId,AssessmentAgencyId,StageId,PartnerId,AssessmentDate){
        LoadAssessmentTypes();
        LoadAssessmentAgency();
        LoadAssessmentPartnerTypes();
        LoadPartner(Partner_Category_Id)
        $('#TxtRequestedDate').val('');
        $('#DivScheduleDate').hide();
        $('#DivAssessmentDate').hide();
        $('#DivAssessorName').hide();
        $('#DivAssessorMob').hide();
        $('#DivAssessorEmail').hide();
        $('#DivCandidates').show();
        AbsentCandidateBatch($('#hdn_batch_assessment_id').val(),AssessmentId,3); 
        $('#TxtScheduledDate').val('');
        $('#TxtAssessmnetDate').val('');
        $('#hdn_batch_assessment_id').val(BatchId);
        $('#ddlAssessmentType').val(AssessmentTypeId);
        $('#ddlAssessmentAgency').val(AssessmentAgencyId).trigger('change');
        $('#hdn_assessment_id').val(AssessmentId);
        $('#ddlPartnerType').val(Partner_Category_Id);
        $('#hdn_current_stage_id').val(StageId);
        $('#ddlPartner').val(PartnerId);
        $('#hdn_reassessment_flag').val(1);
        $('#ddlAssessmentType').attr('disabled', true);
        $('#ddlAssessmentAgency').attr('disabled', true);
        $('#ddlPartner').attr('disabled', true);
        $('#ddlPartnerType').attr('disabled', true);
        $('#TxtRequestedDate').attr('disabled', false);
        $('#mdl_create_batch_assessments').modal('show');
    }
    function EditAssessmentDetails(AssessmentId,Partner_Category_Id,ReqDate,SchDate,AssessmentTypeId,AssessmentAgencyId,StageId,PartnerId,AssessmentDate)
    {
        LoadAssessmentTypes();
        LoadAssessmentAgency();
        LoadAssessmentPartnerTypes();
        LoadPartner(Partner_Category_Id)
        //alert($('#hdn_batch_assessment_id').val());
        //AbsentCandidateBatch($('#hdn_batch_assessment_id').val());

        $('#TxtRequestedDate').val(ReqDate);
        $('#TxtScheduledDate').val(SchDate!='NA'?SchDate:'');
        $('#TxtAssessmnetDate').val(AssessmentDate!='NA'?AssessmentDate:'');
        $('#ddlAssessmentType').val(AssessmentTypeId);
        $('#ddlAssessmentAgency').val(AssessmentAgencyId).trigger('change');
        $('#hdn_assessment_id').val(AssessmentId);
        $('#ddlPartnerType').val(Partner_Category_Id);
        $('#hdn_current_stage_id').val(StageId);
        $('#ddlPartner').val(PartnerId);
        $('#DivCandidates').hide();
        //$('#DivPartnerType').hide();
        
        $('#ddlAssessmentType').prop('disabled', 'disabled');
        $('#ddlAssessmentAgency').prop('disabled', 'disabled');
        $('#ddlPartner').prop('disabled', 'disabled');
        $('#ddlPartnerType').prop('disabled', 'disabled');
        $('#TxtRequestedDate').prop('disabled', 'disabled');

        if (StageId==1)
        {
            $('#DivScheduleDate').show();
            
            $('#DivAssessmentDate').hide();
            $('#DivAssessorName').hide();
            $('#DivAssessorMob').hide();
            $('#DivAssessorEmail').hide();
            $('#DivCandidates').hide();
        }
        else if (StageId==2)
        {
            $('#TxtScheduledDate').prop('disabled', 'disabled'); 
            $('#TxtAssessmentDate').attr('disabled', false);
            $('#DivScheduleDate').show();
            $('#DivAssessmentDate').show();  
            $('#DivAssessorName').show();
            $('#DivAssessorMob').show();
            $('#DivAssessorEmail').show();
            //$('#DivCandidates').show();
            //AbsentCandidateBatch($('#hdn_batch_assessment_id').val(),$('#hdn_assessment_id').val(),StageId);         
        }
        else
        {
            $('#TxtScheduledDate').prop('disabled', 'disabled');   
            $('#TxtAssessmnetDate').prop('disabled', 'disabled'); 
            $('#DivAssessorName').hide();
            $('#DivAssessorMob').hide();
            $('#DivAssessorEmail').hide();  
            $('#DivCandidates').hide();
            
        }

            
        
        
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
                            if(data.AssessmentAgency[i].Assessment_Agency_Id != 3)
                            {
                               $('#ddlAssessmentAgency').append(new Option(data.AssessmentAgency[i].Assessment_Agency_Name,data.AssessmentAgency[i].Assessment_Agency_Id));
                            }
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
    {   console.log($('#ddlPartner').val());
        var DateRequested = new Date($('#TxtRequestedDate').val());
        var DateScheduled = new Date($('#TxtScheduledDate').val());
        var DateAssessed = new Date($('#TxtAssessmentDate').val());
        if($('#hdn_home_user_role_id').val()=="7" )
        {
            if($('#ddlAssessmentType').val() =="2")
            {
                alert("Access Denied FOr Scheduling Summative Assessment.");
                return false; 
            }
        }
        if($('#ddlAssessmentAgency').val()=='2' & $('#ddlPartner').val()=='')
        {
            alert("Please select partner.");
            return false;
        }
        else if($('#TxtRequestedDate').val()=='')
        {
            alert("Please enter proposed date.");
            return false;
        }
        else if($('#hdn_current_stage_id').val()=="1" & $('#TxtScheduledDate').val()=='')
        {
            alert("Please enter assesment confirmed date.");
            return false;
        }
        else if($('#hdn_current_stage_id').val()=="1" & (DateScheduled < DateRequested))
        {
            alert("Assessment Confirmed date can not be less than proposed date.");
            return false;
        }
        else if($('#hdn_current_stage_id').val()=="2" & (DateAssessed < DateScheduled))
        {
            alert("Assesssment date can not be less than Assessment Confirmed date.");
            return false;
        }
        else if($('#hdn_current_stage_id').val()=="2" & $('#TxtAssessmnetDate').val()=='')
        {
            alert("Please enter assessment date.");
            return false;
        }
        /*else if($('#hdn_current_stage_id').val()=="2" & $('#TxtAssessorName').val()=='')
        {
            alert("Please enter assessor name.");
            return false;
        }
        else if($('#hdn_current_stage_id').val()=="2" & $('#TxtAssessorEmail').val()=='')
        {
            alert("Please enter assessor email.");
            return false;
        }*/

        var cand_present='';
        var cand_absent='';
        $('[name=checkcase]').each(function () {
            if (this.checked) {
                cand_absent+= $(this).val()+',';
            }
            else{
                cand_present+= $(this).val()+',';
            }
        });
        cand_present=cand_present.substring(0,cand_present.length-1);
        cand_absent=cand_absent.substring(0,cand_absent.length-1)
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
                    "assessment_date" : $('#TxtAssessmnetDate').val(),
                    "assessment_agency_id" : $('#ddlAssessmentAgency').val(),
                    "assessment_type_id" : $('#ddlAssessmentType').val(),
                    "assessment_id" : $('#hdn_assessment_id').val(),
                    "partner_id" : $('#ddlPartner').val(),
                    "current_stage_id" : $('#hdn_current_stage_id').val(),
                    "Absent_Candidate" : cand_absent,
                    "Present_Candidate" : cand_present,
                    "Assessor_Name" :  $('#TxtAssessorName').val(),
                    "Assessor_Email" :  $('#TxtAssessorEmail').val(),
                    "Assessor_Mobile" :  $('#TxtAssessorMob').val(),
                    "reassessment_flag": $('#hdn_reassessment_flag').val()
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
                                    //GetAssessments($('#hdn_batch_assessment_id').val(),$('#hdn_current_stage_id').val());
                                   // LoadTable();
                                    window.location.href = '/assessment';
                                    $('#mdl_create_batch_assessments').modal('hide');
                                }); 
                },
                error:function(x){
                    alert('error');
                }
            });
    
    }

    function DownloadAssessmentResult(AssessmentId,Batch_Code)
    {         
        //$('#divLoader').show();        
        var URL=$('#hdn_web_url').val()+ "/DownloadAssessmentResult?AssessmentId="+AssessmentId+"&Batch_Code="+Batch_Code ;            
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
    function LoadAssessmentPartnerTypes()
    {
        var URL=$('#hdn_web_url').val()+ "/GetAssessmentPartnerTypes";
            $.ajax({
                type:"GET",
                url:URL,
                async:false,        
                beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
                datatype:"json",
                success: function (data){
                    if(data.AssessmentPartnerTypes != null)
                    {
                        $('#ddlPartnerType').empty();
                        var count=data.AssessmentPartnerTypes.length;
                        if( count> 0)
                        {
                            $('#ddlPartnerType').append(new Option('Choose Assessment Partner Type',''));
                            for(var i=0;i<count;i++)
                                $('#ddlPartnerType').append(new Option(data.AssessmentPartnerTypes[i].Assessment_Partner_Type_Name,data.AssessmentPartnerTypes[i].Assessment_Partner_Type_Id));
                            
                        }
                        else
                        {
                            $('#ddlPartnerType').append(new Option('ALL',''));
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
    
    function AgencyOnChange(AgencyId)
    {
        //LoadPartner();
        if (AgencyId==2)
        {
            LoadAssessmentPartnerTypes();
            $('#DivPartnerType').show();
            $('#ddlPartnerType').prop('Required');
            $('#DivPartner').show();
            $('#ddlPartner').prop('Required');
        }
        else
        {
            $('#DivPartner').hide();
            $('#ddlPartner').removeProp('Required');
            $('#DivPartnerType').hide();
            $('#ddlPartnerType').removeProp('Required');
        }
        
    }

    function PartnetTypeOnChange(PartnerTypeId)
    {
        //alert(PartnerTypeId);
        LoadPartner(PartnerTypeId)
    }
    function LoadPartner(PartnerTypeId)
    {
        var URL=$('#hdn_web_url').val()+ "/GetPartners?PartnerTypeId="+PartnerTypeId;
        //alert(URL);
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                if(data.Partners != null)
                {
                    $('#ddlPartner').empty();
                    var count=data.Partners.length;
                    $('#ddlPartner').append(new Option('Select',''));
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            if(data.Partners[i].Partner_Type_Id==2)
                            $('#ddlPartner').append(new Option(data.Partners[i].Partner_Name,data.Partners[i].Partner_Id));
                    }
                    else
                    {
                        $('#ddlPartner').append(new Option('ALL','-1'));
                    }
                }
            },
            error:function(err)
            {
                alert('Error loading partners! Please try again');
                return false;
            }
        });
    }
    function AbsentCandidateBatch(BatchId,AssessmentId,StageId){
        flag='absent'
        $('#tbl_mark_absent_candidate').show();
        $('#tbl_mark_absent_candidate').dataTable().fnDestroy();    
    
        var URL=$('#hdn_web_url').val()+ "/ALLCandidatesEnrolledInBatch?batch_id="+BatchId+"&assessmentId="+AssessmentId;
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
                $("#tbl_mark_absent_candidate tbody").empty();
                if(!jQuery.isEmptyObject(data))
                {   
                    if (data.Candidates != null){
                        var count=data.Candidates.length;
                        if( count> 0)
                        {   if(StageId==0)
                            {
                                $("#lblCandidateTable").text("Select Not-Eligible Candidates for Assessment:");
                                  }
                            else{
                                $("#lblCandidateTable").text("Select Candidates For Re-Assessment:");
                                  }
                            
                            for(var i=0;i<count;i++)
                            {   
                                
                                var txt=''
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].S_No +'</td>';
                                if(data.Candidates[i].Is_Absent==0) 
                                    txt+='<input id="addedchk" name="checkcase" type="checkbox" value="'+data.Candidates[i].Candidate_Id+'" >';
                                else{
                                    $("#lblCandidateTable").text("Select Candidates For Re-Assessment");
                                    txt+='<input id="addedchk" name="checkcase" type="checkbox" value="'+data.Candidates[i].Candidate_Id+'" checked>';
                                    }
                                varHtml+='  <td style="text-align:center;">'+ txt +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Candidate_Id +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Candidate_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Mobile_Number +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Enrollment_Id +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Attempt +'</td>';
                                varHtml+='</tr>';

                            }                        
                        }
                        $("#tbl_mark_absent_candidate tbody").append(varHtml);
                      
                    }
                    else
                    {
                        varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_mark_absent_candidate tbody").append(varHtml);
                        
                    }
                }
                else
                {
                    varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_mark_absent_candidate tbody").append(varHtml);
                   
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
    function OpenAssessmentList()
    {
        $('#mdl_batch_assessments').modal('show');
    }
    function AssessmentListHistory(AssessmentId)
    { 
        $('#mdl_batch_assessments').modal('hide');
        $('#mdl_batch_assessments_history').modal('show'); 
        var URL=$('#hdn_web_url').val()+ "/GetBatchAssessmentsHistory?AssessmentId="+AssessmentId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                $("#tbl_batch_assessment_history tbody").empty();
                if(!jQuery.isEmptyObject(data))
                {   
                    if (data.Assessments != null){
                        var count=data.Assessments.length;
                        if( count> 0)
                        {
                            for(var i=0;i<count;i++)
                            {   
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].S_No +'</td>';                               
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Batch_Code +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Requested_On +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Scheduled_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Types_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Agency_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Partner_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Assessment_Stage_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.Assessments[i].Attempt +'</td>';
                                varHtml+='</tr>';

                            }                        
                        }
                        $("#tbl_batch_assessment_history tbody").append(varHtml);
                        //$('#mdl_batch_assessments_history').modal('show');
                    }
                    else
                    {
                        varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_batch_assessment_history tbody").append(varHtml);
                        $('#mdl_batch_assessments_history').modal('show');
                    }
                }
                else
                {
                    varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_batch_assessment_history tbody").append(varHtml);
                    $('#mdl_batch_assessments_history').modal('show');
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

    function UploadResult(AssessmentId,BatchId,StageId,BatchCode,ReqDate,SchDate,AssessDate)
    {
        
        $('#HduploadFile').text(BatchCode);
        $('#imgSpinner1').hide();

        $('#TxtReqDate').val(ReqDate);
        $('#TxtSchDate').val(SchDate);
        $('#TxtAssessDate').val(AssessDate);
        $('#hdn_upl_assessment_id').val(AssessmentId);
        $('#hdn_upl_batch_id').val(BatchId);
        $('#hdn_upl_batch_code').val(BatchCode);
        $('#hdn_upl_stage_id').val(StageId);

        $('#hdn_home_user_id_modal').val($('#hdn_home_user_id').val());
        $('#hdn_home_user_role_id_modal').val($('#hdn_home_user_role_id').val());
        $('#mdl_batch_assessments').modal('hide');
        $('#mdl_candidate_result_upload').modal('show');
        $('#myFile').val('');
    }
    function DownloadResultTemplate(AssessmentId,BatchId,StageId,Batch_Code)
    {
        console.log(AssessmentId,BatchId,StageId);
        var URL=$('#hdn_web_url').val()+ "/DownloadAssessmentResultUploadTemplate";            
        $.ajax({
            type:"GET",
            url:URL,
            //async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            data:{  
                     "AssessmentId":AssessmentId,
                     "BatchId":BatchId,
                     "Batch_Code":Batch_Code
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

    
function UploadFileData()
{
    if ($('#myFile').get(0).files.length === 0) {
        console.log("No files selected.");
    }
    else
    {
//        UploadFileToProcess();
//    }
//}
        var fileExtension = ['xlsx']
        if ($.inArray($('#myFile').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            $("#imgSpinner1").show();

            var files=document.getElementById("myFile").files;
            var file=files[0];

            var file_path=$('#hdn_AWS_S3_path').val()+"bulk_upload/assessment/" + $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name;
            var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET",api_url );
                xhr.onreadystatechange = function(){
                    if(xhr.readyState === 4){
                    if(xhr.status === 200){
                        var response = JSON.parse(xhr.responseText);
                        //console.log(response);
                        uploadFileToS3(file, response.data, response.url);
                    }
                    else{
                        alert("Could not get signed URL.");
                    }
                    }
                };
                xhr.send();
        }
    }
}

function uploadFileToS3(file, s3Data, url){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);

    var postData = new FormData();
    for(key in s3Data.fields){
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);

    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4){
        if(xhr.status === 200 || xhr.status === 204){
            var response = xhr;
            //console.log(response);
            UploadFileToProcess();
        }
        else{
            alert("Could not upload file to s3.");
        }
    }
    };
    xhr.send(postData);
}

function UploadFileToProcess()
{
    //console.log()
    var form_data = new FormData($('#formUpload')[0]);
    form_data.append('user_id',$('#hdn_home_user_id_modal').val());
    form_data.append('user_role_id',$('#hdn_home_user_role_id_modal').val());
    form_data.append('assessment_id',$('#hdn_upl_assessment_id').val());
    form_data.append('batch_id',$('#hdn_upl_batch_id').val());
    form_data.append('stage_id',$('#hdn_upl_stage_id').val());
    
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_assessment_result",
        enctype: 'multipart/form-data',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) 
        {
            var message="",title="",icon="";
            if(data.Status){
                message=data.message;
                title="Success";
                icon="success";
            }
            else{
                message=data.message;
                title="Error";
                icon="error";
            }
            swal({   
                        title:title,
                        text:message,
                        icon:icon,
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/assessment';
                        }); 
        },
        error:function(err)
        {
            swal({   
                title:"Error",
                text:'Error! Please try again',
                icon:"error",
                confirmButtonClass:"btn btn-confirm mt-2"
                }).then(function(){
                    window.location.href = '/assessment';
                }); 
           
        }
    });
}

    function Back()
    {
        window.location.href = '/assessment';

    }
    function Reassessment(AssessmentId,BatchId,Partner_Category_Id,ReqDate,SchDate,AssessmentTypeId,AssessmentAgencyId,StageId,PartnerId,AssessmentDate)
    {
        ScheduleReAssessmentModal(AssessmentId,BatchId,Partner_Category_Id,ReqDate,SchDate,AssessmentTypeId,AssessmentAgencyId,StageId,PartnerId,AssessmentDate);

    }