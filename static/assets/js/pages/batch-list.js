var varTable;
var varTable1;
var flag = "";
var role_id;
function showdates(){
    $('#filter_date_box').show();
}

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

function loadBU(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_BU" 
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.BU != null)
            {  
                $('#ddlBU').empty();
                var count=data.BU.length;
                if( count> 0)
                {
                    //$('#ddlClient').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlBU').append(new Option(data.BU[i].Bu_Name,data.BU[i].Bu_Id));
                }
                else
                {
                    $('#ddlBU').append(new Option('ALL','-1'));
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
                   // $('#ddlProject').append(new Option('ALL','-1'));
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
        type:"GET",
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
    vartable = $("#tbl_batchs").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        //"scrollX": true,
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
                d.status = $('#ddlStatus').val().toString();
                d.customer = $('#ddlClient').val().toString();
                d.project = $('#ddlProject').val().toString();
                d.sub_project = $('#ddlSubProject').val().toString();
                d.region = $('#ddlRegion').val().toString();
                d.center = $('#ddlCenter').val().toString();
                d.center_type = $('#ddlCenterType').val().toString();
                d.Planned_actual = $('#Planned_actual').val().toString();
                d.StartFromDate = $('#StartFromDate').val().toString();
                d.StartToDate = $('#StartToDate').val().toString();
                d.EndFromDate = $('#EndFromDate').val().toString();
                d.EndToDate = $('#EndToDate').val().toString();
                d.BU =  $('#ddlBU').val().toString();
            },
            error: function (e) {
                $("#tbl_batchs tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [

            								
            { "data": "S_No"},
            {"visible": ($('#hdn_home_user_role_id').val()=='1'||$('#hdn_home_user_role_id').val()=='5'||$('#hdn_home_user_role_id').val()=='15')?true:false,
            // function (){
            //     if(($('#hdn_home_user_role_id').val() =='1') || ($('#hdn_home_user_role_id').val() =='5')||($('#hdn_home_user_role_id').val() =='15'))
            //         return true;
            //     else return false;
            // },
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if($('#hdn_home_user_role_id').val()=='1')
                {
                    varButtons += '<a onclick="CancelActualBatch(\'' + row.Batch_Id + '\')" class="btn" style="cursor:pointer" ><i title="Cancel Batch" class="fas fa-cut" ></i></a>';
                
                }
                varButtons += '<a onclick="EditBatchDetail(\'' + row.Batch_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Batch" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Batch_Code"},
            { "data": "Planned_Batch_Code"},
            { "data": "Start_Date" },
            { "data": "End_Date" },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Candidate_Count=="" || row.Candidate_Count=="0")
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Candidate_Count;
                        }
                    
                    else
                    {   //console.log(row.Trainer_Id)
                        //console.log(row.Center_Id);
                        //varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id +  '\' )"  style="color:blue;cursor:pointer" >' + row.Center_Id + '</a>';
                        varButtons += '<a onclick="GetCandidate_Detail(\'' + row.Batch_Id + '\',\'' + row.Project_Type + '\' )"  style="color:blue;cursor:pointer" >' + row.Candidate_Count + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Center_Name=="")
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Center_Name;
                        }
                        
                    else
                    {   
                        //console.log(row.Center_Id);
                        //varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id +  '\' )"  style="color:blue;cursor:pointer" >' + row.Center_Id + '</a>';
                        varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id + '\',\'' + row.Center_Name + '\' )"  style="color:blue;cursor:pointer" >' + row.Center_Name + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            //{ "data": "Center_Name" },
            //{ "data": "Course_Name" },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = "";
                    if(row.Course_Name=="")
                        {
                            varButtons=row.Course_Name;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetCourseDetail(\'' + row.Course_Id +  '\' )"  style="color:blue;cursor:pointer" >' + row.Course_Name + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            { "data": "Status"},
            { "data": "Batch_Name" },
            { "data": "Product_Name" },
            { "data": "Sub_Project_Name" },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Trainer_Email=="")
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Trainer_Email;
                        }
                    
                    else
                    {   //console.log(row.Trainer_Id)
                        //console.log(row.Center_Id);
                        //varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id +  '\' )"  style="color:blue;cursor:pointer" >' + row.Center_Id + '</a>';
                        varButtons += '<a onclick="GetUserDetail(\'' + row.Trainer_Id + '\',\'' + 'trainer' + '\' )"  style="color:blue;cursor:pointer" >' + row.Trainer_Email + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            //{ "data": "Trainer_Email" },
            { "data": "Center_Manager_Email" },
            
            { "data": "Start_Time"},
            { "data": "End_Time"}
            
        ],
        'columnDefs': [ {

            'targets': [1,5,4], /* column index */
    
            'orderable': false, /* true or false */
    
         }],
        //"scrollX": true,

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

function CancelBatchSubmit(batch_id)
{
    //alert(batch_id);
    if ($('#TxtReason').val()=='')
    {
        alert('Please Enter Reason To Cancel The Batch.');
    }
    else
    {
       var URL=$('#hdn_web_url').val()+ "/cancel_actual_batch";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "user_id": $('#hdn_home_user_id').val(),
                    "actual_batch_id": batch_id,
                    "cancel_reason": $('#TxtReason').val()
                },
                success:function(data){
                    if(data.PopupMessage.message =="Batch Cancelled")
                    {
                        swal({   
                            title:data.PopupMessage.message,
                            text:data.PopupMessage.message+" Sucessfully!!",
                            icon:"success",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/batch';                          
                            });

                    }
                    else{
                        swal({   
                            title:data.PopupMessage.message,
                            text:"Error!",
                            icon:"error",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                               window.location.href = '/sub_project';                          
                            });
                    }
                        
                },
                error:function(err)
                {
                    alert('Error! Please try again');
                    return false;
                }
            });
    }
}

function CancelActualBatch(batch_id)
{
    $('#hdn_actual_batch').val(batch_id);
    $('#mdl_cancel_batch').modal('show');
    
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
    if($('#txtremark').val()=='')
    {
        alert('Please enter reason.');
    }
    else
    {
        var URL=$('#hdn_web_url').val()+ "/drop_edit_candidate_batch";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "course_id": 0,
                    "skilling_ids": $('#hdn_mdl_skilling_id').val(),
                    "batch_id": $('#hdn_mdl_batch_id').val(),
                    "drop_remark": $('#txtremark').val(),
                    "user_id":$('#hdn_home_user_id').val()
                },
                success:function(data){
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" Successfully !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/batch';
                        });
                },
                error:function(err)
                {
                    alert('Error! Please try again');
                    return false;
                }
            });
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
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" Done Successfully !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/after_popup_batch';
                        });
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
                        swal({   
                            title:data.PopupMessage.message,
                            text:data.PopupMessage.message+" Done Successfully !!",
                            icon:"success",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/after_popup_batch';
                            });
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

        function GetCandidate_Detail(batch_id,project_type){
            //alert(Project_Id)
            $('#con_close_modal').modal('hide');
            $('#sponser_modal').modal('hide');                              
            
            var URL=$('#hdn_web_url').val()+ "/Getcandidatebybatch?batch_id="+batch_id;
            $.ajax({
                type:"GET",
                url:URL,
                async:false,
                overflow:true,        
                beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
                datatype:"json",
                success: function (data){
                    varHtml='';
                    $("#tblcandidate_details").dataTable().fnDestroy();
                    $("#tblcandidate_details tbody").empty();
                    if(!jQuery.isEmptyObject(data.candidates))
                    {   //alert(data.Customer_Name)
                        $('#txtbatch_name').val(data.batch_name);
                        $('#txtcenter_name').val(data.center_name);
                        $('#txtcourse_name').val(data.course_name);
                        if (data.candidates != null){
                        if (data.candidates[0].Candidate_Name != null){
                            var count=data.candidates.length;
                            if( count> 0)
                            {
                                for(var i=0;i<count;i++)
                                {
                                    varHtml+='<tr>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].S_No +'</td>';
                                    varHtml += '<td style="text-align:center;"><input id="addedchk1" name="checkcase1" type="checkbox" value="'+data.candidates[i].Skilling_Id+'" ></td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Intervention_Value +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Candidate_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Date_Of_Birth +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Gender +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Mobile_Number +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Email_Id +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Father_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Annual_Income +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.candidates[i].Sponsers +'</td>';
                                    varHtml+='</tr>';
                                }
                                
                            }
                            $("#tblcandidate_details tbody").append(varHtml);
                            $("#tblcandidate_details").DataTable( {
                                "columnDefs": [
                                    {
                                        "targets": [10],
                                        "visible": false
                                    }
                                ]
                            });
                            if(project_type.toString() == "2")
                            {
                                $('#btnSponser').show();
                                $("#tblcandidate_details").DataTable().column(10).visible(true);

                            }
                            else
                            {
                                $('#btnSponser').hide();
                                $("#tblcandidate_details").DataTable().column(10).visible(false);
                            }
                            $('#tr_candidate_detail').modal('show');                            
                            $('#hdn_mdl_batch_id').val(batch_id);
                        }
                        else
                        {
                            varHtml='<tr><td colspan="9" style="text-align:center;">No records found</td></tr>'
                            $("#tblcandidate_details tbody").append(varHtml);
                            $('#tr_candidate_detail').modal('show');
                        }
                        }
                        else
                        {
                            varHtml='<tr><td colspan="9" style="text-align:center;">No records found</td></tr>'
                                $("#tblcandidate_details tbody").append(varHtml);
                                $('#tr_candidate_detail').modal('show');
                        }

                    }
                    else
                    {
                        varHtml='<tr><td colspan="9" style="text-align:center;">No records found</td></tr>'
                        $("#tblcandidate_details tbody").append(varHtml);
                        $('#tr_candidate_detail').modal('show');
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
                    varHtml='';
                    $("#tblsubproject_details").dataTable().fnDestroy();
                    $("#tblsubproject_details tbody").empty();
                    if(!jQuery.isEmptyObject(data.CourseDetail))
                    {   //alert(data.Customer_Name)
                        $('#txtCourse_Code').val(data.Course_Code);
                        $('#txtCourse_Name').val(data.Course_Name);
                        if (data.CourseDetail[0].Sub_Project_Name != null){
                            var count=data.CourseDetail.length;
                            if( count> 0)
                            {
                                for(var i=0;i<count;i++)
                                {   
                                    varHtml+='<tr>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].S_No +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].Project_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].Sub_Project_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].Sub_Project_Code +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].Product_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].Region_Name +'</td>';
                                    varHtml+='  <td style="text-align:center;">'+ data.CourseDetail[i].State_Name +'</td>';
                                    varHtml+='</tr>';
                                }
                                
                            }
                            $("#tblsubproject_details tbody").append(varHtml);
                            $("#tblsubproject_details").DataTable();
                            $('#course_details_modal').modal('show');
                        }
                        else
                    {
                        varHtml='<tr><td colspan="3" style="text-align:center;">No records found</td></tr>'
                        $("#tblsubproject_details tbody").append(varHtml);
                        $('#course_details_modal').modal('show');
                    }
                    }
                    else
                    {
                        varHtml='<tr><td colspan="3" style="text-align:center;">No records found</td></tr>'
                        $("#tblsubproject_details tbody").append(varHtml);
                        $('#course_details_modal').modal('show');
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
    function DropCandidates()
    {
        var cands='';
        $('[name=checkcase1]:checked').each(function () {
            cands+= $(this).val()+',';
        });
        cands=cands.substring(0,cands.length-1)
        if (cands=='')
        {
            alert('Select at least one candidate to drop.');
        }
        else
        {
            $('#hdn_mdl_skilling_id').val(cands);
            $('#tr_candidate_detail').modal('hide');
            $('#con_close_modal').modal('show');
        }
    }
    function back()
    {
        GetCandidate_Detail($('#hdn_mdl_batch_id').val(),1);
    }
    function TagSponser()
    {
        var cands='';
        $('[name=checkcase1]:checked').each(function () {
            cands+= $(this).val()+',';
        });
        cands=cands.substring(0,cands.length-1)
        if (cands=='')
        {
            alert('Select at least one candidate to Tag.');
        }
        else
        {
            $('#tr_candidate_detail').modal('hide');            
            $('#hdn_mdl_skilling_id').val(cands);
            loadSponsers();
            $('#sponser_modal').modal('show');
        }
    }

    function loadSponsers()
    {
        var URL=$('#hdn_web_url').val()+ "/Get_all_Sponser" 
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                if(data.Sponser != null)
                {  
                    $('#ddlSponser').empty();
                    var count=data.Sponser.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            $('#ddlSponser').append(new Option(data.Sponser[i].Sponser_Name,data.Sponser[i].Sponser_Id));
                    }
                    else
                    {
                        $('#ddlSponser').append(new Option('ALL','-1'));
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

    function tagSponserSubmit()
    {
        if($('#ddlSponser').val()=='' || $('#ddlSponser').val()=='-1')
        {
            alert('Please select atleast on sponser.');
        }
        else
        {
            var URL=$('#hdn_web_url').val()+ "/tag_sponser_candidate";
            $.ajax({
                    type:"POST",
                    url:URL,
                    data:{
                        "skilling_ids": $('#hdn_mdl_skilling_id').val(),
                        "sponser_ids": $('#ddlSponser').val().toString(),
                        "user_id":$('#hdn_home_user_id').val()
                    },
                    success:function(data){
                        swal({   
                            title:data.PopupMessage.message,
                            text:data.PopupMessage.message+" successfully !!",
                            icon:"success",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                GetCandidate_Detail($('#hdn_mdl_batch_id').val(),2)
                               
                                //window.location.href = '/batch';
                            });
                    },
                    error:function(err)
                    {
                        alert('Error! Please try again');
                        return false;
                    }
                });
        }
    }
    function DownloadTableBasedOnSearch(){
        $("#imgSpinner").show();
        /*if($('#ddlCustomer').val()==''|| $('#ddlCustomer').val()==null){
            alert("Please select a Customer.");
        
        }
        else if($('#ddlCenter').val()==''|| $('#ddlCenter').val()==null){
            alert("Please select a Center.");
        
        }
        else if($('#ddlCourse').val()==''|| $('#ddlCourse').val()==null){
            alert("Please select a Center.");
        
        }
        */
        if (0==9){
        console.log(false)
        }
        else{
            var URL=$('#hdn_web_url').val()+ "/batch_download_report"
            //window.location = URL + "?ActivityDate=2019-09-09"
            $.ajax({
                        type: "POST",
                        dataType: "json",
                        url: URL, 
                        data: {
                                'batch_id':0,
                                'user_id':$('#hdn_home_user_id').val(),
                                'user_role_id':$('#hdn_home_user_role_id').val(),
                                'status':$('#ddlStatus').val().toString(),
                                'customer':$('#ddlClient').val().toString(),
                                'project': $('#ddlProject').val().toString(),
                                'sub_project':$('#ddlSubProject').val().toString(),
                                'region':$('#ddlRegion').val().toString(),
                                'center':$('#ddlCenter').val().toString(),
                                'center_type':$('#ddlCenterType').val().toString(),
                                'BU':$('#ddlBU').val().toString(),
                                'Planned_actual' :$('#Planned_actual').val().toString(),
                                'StartFromDate' :$('#StartFromDate').val().toString(),
                                'EndFromDate' :$('#EndFromDate').val().toString(),
                                'EndToDate' :$('#EndToDate').val().toString(),
                                'StartToDate' :$('#StartToDate').val().toString()
    
                        },
                        success: function(resp) 
                        {
    
                            if (resp.Status){
                                var varAnchor = document.getElementById('lnkDownload');
                                varAnchor.href = $('#hdn_web_url').val() + '/report file/' + resp.filename;
                                $("#imgSpinner").hide();
                                try 
                                    { 
                                        //in firefox
                                        varAnchor.click();
                                        return;
                                    } catch(ex) {}
                                    
                                    try 
                                    { 
                                        // in chrome
                                        if(document.createEvent) 
                                        {
                                            var e = document.createEvent('MouseEvents');
                                            e.initEvent( 'click', true, true );
                                            varAnchor.dispatchEvent(e);
                                            return;
                                        }
                                    } catch(ex) {}
                                    
                                    try 
                                    { 
                                        // in IE
                                        if(document.createEventObject) 
                                        {
                                             var evObj = document.createEventObject();
                                             varAnchor.fireEvent("onclick", evObj);
                                             return;
                                        }
                                    } catch(ex) {}
                                
                            }
                            else{
                                //alert(resp.Description)
                                //alert('Not success')
                                $("#imgSpinner").hide();
                                
                            }
                        },
                        error:function()
                        {
                            //$("#imgSpinner").hide();
                        }
                    });
            
        }
        //$("#imgSpinner").hide();
    }
    function DownloadCandidateTableBasedOnSearch(){
        $("#imgSpinner").show();
        if (0==9){
        console.log(false)
        }
        else{
            var URL=$('#hdn_web_url').val()+ "/batchcandidate_download_report"
            //window.location = URL + "?ActivityDate=2019-09-09"
            $.ajax({
                        type: "POST",
                        dataType: "json",
                        url: URL, 
                        data: {
                                'batch_id':$('#hdn_mdl_batch_id').val()
                        },
                        success: function(resp) 
                        {
    
                            if (resp.Status){
                                var varAnchor = document.getElementById('lnkDownload');
                                varAnchor.href = $('#hdn_web_url').val() + '/report file/' + resp.filename;
                                $("#imgSpinner").hide();
                                try 
                                    { 
                                        //in firefox
                                        varAnchor.click();
                                        return;
                                    } catch(ex) {}
                                    
                                    try 
                                    { 
                                        // in chrome
                                        if(document.createEvent) 
                                        {
                                            var e = document.createEvent('MouseEvents');
                                            e.initEvent( 'click', true, true );
                                            varAnchor.dispatchEvent(e);
                                            return;
                                        }
                                    } catch(ex) {}
                                    
                                    try 
                                    { 
                                        // in IE
                                        if(document.createEventObject) 
                                        {
                                             var evObj = document.createEventObject();
                                             varAnchor.fireEvent("onclick", evObj);
                                             return;
                                        }
                                    } catch(ex) {}
                                
                            }
                            else{
                                //alert(resp.Description)
                                //alert('Not success')
                                $("#imgSpinner").hide();
                                
                            }
                        },
                        error:function()
                        {
                            //$("#imgSpinner").hide();
                        }
                    });
            
        }
        //$("#imgSpinner").hide();
    }
    function ForceDownload(varUrl, varFileName)
            {
                var link = document.createElement('a');
                link.setAttribute('href', varUrl);
                link.setAttribute('download', varFileName);
                link.setAttribute('target', '_blank');
                link.style.display = 'none';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }