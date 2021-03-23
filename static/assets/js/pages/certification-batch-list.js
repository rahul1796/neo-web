var varTable;
var varTable1;
var flag = "";
var role_id;
var check_list = [];

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
            "url": $('#hdn_web_url').val()+ "/batch_list_certification",
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
                d.assessment_stage_id= "4";                
                d.certification_stage_id= $('#ddlCertificationStages').val().toString();
            },
            error: function (e) {
                $("#tbl_batchs tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [

            								
            { "data": "S_No"},
            { "orderable":false,
              "visible": true,
                "data": function(row, type, val, meta) {
                    var varButtons='';
                    if(((row.Planned_Distribution>0) || (row.Distributed_Count>0))&($('#hdn_home_user_role_id').val()=='1'||$('#hdn_home_user_role_id').val()=='5'))
                        varButtons+='<a onclick="UploadBatchImage(\'' + row.Batch_Id + '\',\'' + row.Batch_Code + '\')" class="btn" style="cursor:pointer" ><i title="Upload Batch Image" class="fe-upload" ></i></a>';
                    if(row.Batch_Image!= '')
                        varButtons+='<a onclick="DownloadCertificationImage(\'' + row.Batch_Image + '\',)" class="btn" style="cursor:pointer" ><i title="Download Batch Image" class="fe-download" ></i></a>';
                    
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
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Passed==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Passed;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 0 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Passed + '</a>';
                    }
                    return varButtons;
                    return row.Passed;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Result_Verified==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Result_Verified;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 7 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Result_Verified + '</a>';
                    }
                    return varButtons;
                   // return row.Result_Verified;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Rfm_Result==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Rfm_Result;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 8 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Rfm_Result + '</a>';
                    }
                    return varButtons;
                    //return row.Result_Verified;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Soft_Copy_Upload==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Soft_Copy_Upload;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 9 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Soft_Copy_Upload + '</a>';
                    }
                    return varButtons;
                    //return row.Result_Verified;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Soft_Copy_Approved==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Soft_Copy_Approved;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 10 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Soft_Copy_Approved + '</a>';
                    }
                    return varButtons;
                   // return row.Result_Verified;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Rfm_Soft_Copy==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Rfm_Soft_Copy;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 11 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Rfm_Soft_Copy + '</a>';
                    }
                    return varButtons;
                    // row.Result_Verified;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Requested_Printing==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Requested_Printing;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 1 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Requested_Printing + '</a>';
                    }
                    return varButtons;
                    return row.Requested_Printing;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Sent_Printing==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Sent_Printing;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 2 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Sent_Printing + '</a>';
                    }
                    return varButtons;
                    return row.Sent_Printing;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Sent_Center==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Sent_Center;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 3 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Sent_Center + '</a>';
                    }
                    return varButtons;
                    return row.Sent_Center;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Received_Center==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Received_Center;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 4 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Received_Center + '</a>';
                    }
                    return varButtons;
                    return row.Received_Center;
                    }
            },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Planned_Distribution==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Planned_Distribution;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 5 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Planned_Distribution + '</a>';
                    }
                    return varButtons;
                    return row.Planned_Distribution;
                    }
            },
           
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Distributed_Count==0)
                        {
                            //console.log(row.Center_Id);
                            varButtons=row.Distributed_Count;
                        }
                    
                    else
                    {   
                        varButtons += '<a onclick="GetPassedCandidates(\'' + row.Batch_Id + '\',\'' + 6 + '\', \'' + row.Batch_Code + '\')"  style="color:blue;cursor:pointer" >' + row.Distributed_Count + '</a>';
                    }
                    return varButtons;
                    return row.Distributed_Count;
                    }
            },
        ],
        drawCallback: function(){
            $('#tbl_batchs_paginate ul.pagination').addClass("pagination-rounded");
        }
    });
}
function LoadCertificationStages(){
    var URL=$('#hdn_web_url').val()+ "/AllCertificationStages"
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
            if(data.CertificationStages != null)
            {
                $('#ddlCertificationStages').empty();
                $('#ddlCertificationStages').append(new Option('ALL Stages','0'));
                var count=data.CertificationStages.length;
                if( count> 0)
                {
                  
                   for(var i=0;i<count;i++)
                        $('#ddlCertificationStages').append(new Option(data.CertificationStages[i].Certification_Stage_Name,data.CertificationStages[i].Certification_Stage_Id));
                }
                else
                {
                    $('#ddlCertificationStages').append(new Option('ALL',''));
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

function EditBatchDetail(BatchId)
{
    $('#hdn_batch_id').val(BatchId);
    $('#form1').submit();
    
}
function ShowCandidateCertificationMetrics(Batch_Code,Stage)
    {   
        let txt="Candidate Certification: "+ Batch_Code;
        $('#divBtns').show();
        $('#headBatch').text(txt);
        $('#btnAssessmentInfo').show();
        $('#divAssessmentlist').hide();
        $('#divBillingMetrics').show();
        LoadCandidateCertificateInfo();
        //GetCentersBasedOnSubProjects();
    }
function ShowAssessmentPage()
{
    LoadTable();
    $('#headBatch').text("Assessment Batch List");
    $('#divBtns').hide();
    $('#btnAssessmentInfo').hide();
    $('#divAssessmentlist').show();
    $('#divBillingMetrics').hide();
}
function LoadLogisticUsers(){
   var URL=$('#hdn_web_url').val()+ "/GetUsersBasedOnRole?user_role_id=40"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Users != null)
            {
                $('#ddlLogisticUsers').empty();
                var count=data.Users.length;
                if( count> 0)
                {
                    $('#ddlLogisticUsers').append(new Option("--Select--","0"));
                     for(var i=0;i<count;i++)
                        $('#ddlLogisticUsers').append(new Option(data.Users[i].User_Name,data.Users[i].User_Id));
                   
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
function GetPassedCandidates(BatchId,Stage,Batch_Code){   
    $("#tbl_candidate tbody").empty();
    $('#tr_candidate_detail').modal('show');      
    $('#tbl_candidate').show();
    $('#tbl_candidate').dataTable().fnDestroy();  
    $('#hdn_batch_id').val(BatchId);
    $('#hdn_cert_stage_id').val(Stage.toString());
    $('#hdn_batch_code').val(Batch_Code);
    if((Stage==0) & (($('#hdn_home_user_role_id').val()=='15')||($('#hdn_home_user_role_id').val()=='1')))
    {   
        $('#btnStatusChange').show();

    } 
    else if((Stage==9) & (($('#hdn_home_user_role_id').val()=='15')||($('#hdn_home_user_role_id').val()=='1')))
    {   
        $('#btnStatusChange').show();

    } 
    else if((Stage==10) & (($('#hdn_home_user_role_id').val()=='27')||($('#hdn_home_user_role_id').val()=='1')))
    {
        $('#btnUploadCertificate').show();
        $('#btnStatusChange').hide();

    }
    else
    {   
        $('#btnUploadCertificate').hide();
        
        if((Stage==1) &(($('#hdn_home_user_role_id').val()=='40')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').show();
        }
        else if(((Stage==7)|| (Stage==11)) &(($('#hdn_home_user_role_id').val()=='40')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').hide();
            $('#btnBulkUploadCertificate').show();
        }
        else if((Stage==2) &(($('#hdn_home_user_role_id').val()=='40')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').show();
            $('#btnBulkUploadCertificate').hide();
            $('#btnBulkDownloadCertificate').show();
        }
        else if((Stage==3) &(($('#hdn_home_user_role_id').val()=='5')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').show();
           $('#btnBulkDownloadCertificate').show();
        }
        else if((Stage==4) &(($('#hdn_home_user_role_id').val()=='5')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').show();
           $('#btnBulkDownloadCertificate').show();
        }
        else if((Stage==5) &(($('#hdn_home_user_role_id').val()=='5')||($('#hdn_home_user_role_id').val()=='1')))
        {
            $('#btnStatusChange').show();
            $('#btnBulkDownloadCertificate').show();
        }
        else{
            $('#btnStatusChange').hide();
            $('#btnBulkDownloadCertificate').show();
        }
        
    }
   

    var URL=$('#hdn_web_url').val()+ "/ALLCandidatesBasedOnCertifiactionStage?batch_id="+BatchId+"&stage_id="+Stage;
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
            $("#tbl_candidate tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   
                if (data.Candidates != null){
                    var count=data.Candidates.length;
                    if( count> 0)
                    {   
                        for(var i=0;i<count;i++)
                        {   
                            
                            var txt=''
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].S_No +'</td>';
                            if((data.Candidates[i].Certificate_Flag) || (Stage==6)) 
                                 txt += ''
                                else{
                                 txt+='<input id="candcheckcase" name="candcheckcase" type="checkbox" value="'+data.Candidates[i].Intervention_Value+'" >';
                                }
                            varHtml+='  <td style="text-align:center;">'+ txt +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Candidate_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Mobile_Number +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Email_Id +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Intervention_Value +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Score +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Result +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Assessment_Status +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Candidates[i].Certificate_Number +'</td>';
                            varCerti='';
                            varCerti += '<a onclick="DownloadCertificate(\'' + data.Candidates[i].Certificate_Copy +  '\' )"  style="color:blue;cursor:pointer" >' + data.Candidates[i].Certificate_Copy + '</a>';
                            varHtml+='  <td style="text-align:center;">'+ varCerti +'</td>';
                            varCandImage='';
                            varCandImage += '<a onclick="DownloadCertificationImage(\'' +  data.Candidates[i].Uploaded_Cand_Image +  '\' )"  style="color:blue;cursor:pointer" >' +  data.Candidates[i].Uploaded_Cand_Image + '</a>';
                            varHtml+='  <td style="text-align:center;">'+ varCandImage +'</td>';
                            var action='';
                            if((Stage==5) & (($('#hdn_home_user_role_id').val()=='5')||($('#hdn_home_user_role_id').val()=='1')))
                            {
                                action+='<a onclick="UploadCandImage(\'' + data.Candidates[i].Intervention_Value + '\')" class="user-btn" style="cursor:pointer" ><i title="Upload Candidate Image" class="fe-upload" ></i></a>';
                            }
                            if((Stage==7 ||Stage==11) & (($('#hdn_home_user_role_id').val()=='40')||($('#hdn_home_user_role_id').val()=='1')))
                            {
                                action+='<a onclick="UploadCandCertificate(\'' + data.Candidates[i].Intervention_Value + '\')" class="user-btn" style="cursor:pointer" ><i title="Upload Candidate Certificate" class="fe-upload" ></i></a>';
                            }
                            varHtml+='  <td style="text-align:center;">'+ action +'</td>';
                            varHtml+='</tr>';

                        }                        
                    }
                    $("#tbl_candidate tbody").append(varHtml);
                  
                }
                else
                {
                    varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_candidate tbody").append(varHtml);
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="8" style="text-align:center;">No records found</td></tr>'
                $("#tbl_candidate tbody").append(varHtml);
               
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
function UploadCertificate()
{
    
    
   $('#tr_candidate_detail').modal('hide');
    LoadLogisticUsers();
    $('#mdl_certificate_upload').modal('show');
    
}
function BulkUploadCertificate()
{
    
    
   $('#tr_candidate_detail').modal('hide');
    $('#mdl_bulk_certificate_upload').modal('show');
    
}

function toggleCheckbox(e)
    {
       var temp=e.target.getAttribute('value');
       if($('#'+e.target.getAttribute('id')).is(':checked'))
        {
            $('[name=candcheckcase]').each(function () {
                 $(this).prop("checked", true);
            });
        }
        else
        {
            $('[name=candcheckcase]').each(function () {
                $(this).prop("checked", false);
           });
        }
        //console.log(check_list)
    }
function toggleCandidateCheckbox(e)
{
    var temp=e.target.getAttribute('value');
    if($('#'+e.target.getAttribute('id')).is(':checked'))
    {
        alert("True");
        if(jQuery.inArray( temp, check_list )==-1){
            check_list.push(temp);
        }
    }
    else
    {
        if(jQuery.inArray( temp, check_list )!=-1){
            check_list = $.grep(check_list, function(value) {
                return value != temp;
                })
            //check_list = check_list.pop(temp);
        }
    }
    //console.log(check_list)
}

function DownloadCertificateTemplate(){
    $("#imgSpinner1").show();
    var enrollments='';
    $('[name=candcheckcase]').each(function () {
        if($(this).prop('checked') == true)
        {
            enrollments+= $(this).val()+',';
        }
        
    });
    enrollments=enrollments.substring(0,enrollments.length-1)
    var cands=enrollments.toString();
    $("#hdn_enrol_ids").val(cands);
    //alert(cands);
    //cands=cands.substring(0,cands.length-1)
    if ((cands.toString().length)==0)
    {
        alert('Please select candidates:')
        $("#imgSpinner1").hide();
    }
    else{
        var URL=$('#hdn_web_url').val()+ "/DownloadCertificationTemplate"
        //window.location = URL + "?ActivityDate=2019-09-09"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                            //candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                            'user_id':$('#hdn_home_user_id').val(),
                            'user_role_id':$('#hdn_home_user_role_id').val(),
                            'batch_id':$('#hdn_batch_id').val(),
                            'intervention_values':cands.toString()
                    },
                    success: function(resp) 
                    {
                        //console.log(resp)
                        if (resp.Status){
                            var varAnchor = document.getElementById('lnkDownload');
                            window.location='/Bulk Upload/'+ resp.filename;
                            //varAnchor.href = $('#hdn_web_url').val() + '/Bulk Upload/' + resp.filename;
                            $("#imgSpinner1").hide();
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
                                        $("#imgSpinner1").hide();
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
                                         $("#imgSpinner1").hide();
                                         return;
                                    }
                                } catch(ex) {}
                            
                        }
                        else{
                            alert(resp.Description)
                            //alert('Not success')
                            $("#imgSpinner1").hide();
                            
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

function UploadcertificateFileData()
{  
 
     if ($('#ddlLogisticUsers').val()=="0") 
    {
          alert("Please select user to assign stage.");
          return;
    }
    
    if ($('#myFile').get(0).files.length === 0) {
        alert("No files selected.");
        return;
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
            $("#imgSpinner").show();

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
                        $("#imgSpinner").hide();
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
    //form_data.append('user_id',$('#hdn_home_user_id_modal').val());
    form_data.append('assigned_user_id',$('#ddlLogisticUsers').val());
    form_data.append('batch_code',$('#hdn_batch_code').val());
    form_data.append('batch_id',$('#hdn_batch_id').val());
    form_data.append('enrollment_ids', $('#hdn_enrol_ids').val()); 
    
    
    
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_assessment_certificate_number",
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
                            window.location.href = '/certification';
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
function LoadCertificationStageOnSelectedStage()
{
    if ($('#hdn_cert_stage_id').val().toString()=='0')
    {
        if($('#ddlResultStages').val().toString()=='8')
        {
            $('#TxtCertStages').val('Requested For Modification(Result)');
            $('#DivRemarks').show();
        }
        if($('#ddlResultStages').val().toString()=='7')
        {
        
                $('#TxtCertStages').val('Result Confirmed');
                $('#DivRemarks').hide();
            
        }
    }
    else 
    {
        if($('#ddlSoftCopyStages').val().toString()=='11')
        {
            $('#TxtCertStages').val('Requested For Modification(Soft Copy)');
            $('#DivRemarks').show();
        }
        if($('#ddlSoftCopyStages').val().toString()=='10')
        {
        
                $('#TxtCertStages').val('Soft Copy Approved');
                $('#DivRemarks').hide();
            
        }
    }
    
}
function ChangeStage(){
    var enrollments='';
    $('[name=candcheckcase]').each(function () {
        if($(this).prop('checked') == true)
        {
            enrollments+= $(this).val()+',';
        }
        
    });
    enrollments=enrollments.substring(0,enrollments.length-1)
    var cands=enrollments.toString();
    if ((cands.toString().length)==0)
    {
        alert('Please select candidates:')
        return;
       
    }
    $('#DivSentPrintingDate').hide();
    $('#DivSentCenterDate').hide();
    $('#DivCenterExpArrivalDate').hide();
    $('#DivReceivedDate').hide();
    $('#DivPlannedDistributionDate').hide();
    $('#DivActualDistributionDate').hide();
    $('#DivCGName').hide();
    $('#DivCGDesig').hide();
    $('#DivCGOrg').hide();
    $('#DivCGOrgLoc').hide();
    $('#DivResultVerify').hide();
    $('#DivRemarks').hide();
    
    switch (($('#hdn_cert_stage_id').val().toString())) {        
        case "1":
            $('#DivSentPrintingDate').show(); 
            $('#TxtCertStages').val('Sent For Printing');
            break;
        case "0":
            $('#DivResultVerify').show();
            $('#ddlResultStages').empty();
            $('#ddlResultStages').append(new Option('Result Confirmed','7'));
            $('#ddlResultStages').append(new Option('Requested For Modification(Result)','8'));
       
            $('#TxtCertStages').val('Result Confirmed');
            break;
        case "9":
            $('#DivSoftCopyVerify').show();
            $('#ddlSoftCopyStages').empty();
            $('#ddlSoftCopyStages').append(new Option('Soft Copy Approved','10'));
            $('#ddlSoftCopyStages').append(new Option('Requested For Modification(Soft Copy)','11'));
        
            $('#TxtCertStages').val('Soft Copy Approved');
            break;
        case "7":
            $('#TxtCertStages').val('Soft Copy Uploaded');
            break;
        case "2":
            $('#TxtCertStages').val('Sent To Center');
            $('#DivSentCenterDate').show();
            $('#DivCenterExpArrivalDate').show();
            $('#DivCourierNumber').show();
            $('#DivCourierName').show();
            $('#DivCourierUrl').show();
            break;
        case "3":
            $('#TxtCertStages').val('Received By Center');
            $('#DivReceivedDate').show();
            break;
        case "4":
            $('#TxtCertStages').val('Plaaned For Distribution');
            $('#DivPlannedDistributionDate').show();
            $('#DivCGName').show();
            $('#DivCGDesig').show();
            $('#DivCGOrg').show();
            $('#DivCGOrgLoc').show();
            break;
        case "5":
            $('#TxtCertStages').val('Distributed');
            $('#DivActualDistributionDate').show();
           
            break;
    }   
    $('#tr_candidate_detail').modal('hide');
    $('#mdl_certification_status_change').modal('show');
}
function ChangeCertificationStage()
{
    var enrollments='';
    $('[name=candcheckcase]').each(function () {
        if($(this).prop('checked') == true)
        {
            enrollments+= $(this).val()+',';
        }
        
    });
    enrollments=enrollments.substring(0,enrollments.length-1)
    var cands=enrollments.toString();
    if(!(($('#hdn_home_user_role_id').val()=="5") || ($('#hdn_home_user_role_id').val()=="40") || ($('#hdn_home_user_role_id').val()=="1") || ($('#hdn_home_user_role_id').val()=="15")) )
    {
        
            alert("Access Denied FOr Changing Certification Stage.");
            return false; 
       
    }
    else if(($('#hdn_cert_stage_id').val().toString()=="9") & ($('#ddlSoftCopyStages').val().toString()=="11") &($('#TxtRemark').val()==''))
    {
        alert("Please enter Remark.");
        return false;
    }
    else if(($('#hdn_cert_stage_id').val().toString()=="1") & ($('#TxtSentPrintingDate').val()==''))
    {
        alert("Please enter sent for printing date.");
        return false;
    }
    else if(($('#hdn_cert_stage_id').val().toString()=="0") & ($('#ddlResultStages').val().toString()=="8") &($('#TxtRemark').val()==''))
    {
        alert("Please enter Remark.");
        return false;
    }
   
    else if($('#hdn_cert_stage_id').val().toString()=="2" & $('#TxtSentCenterDate').val()=='')
    {
        alert("Please enter sent to center date.");
        return false;
    }
    else if($('#hdn_cert_stage_id').val().toString()=="2" & $('#TxtCourierName').val()=='')
    {
        alert("Please enter courier comapny name.");
        return false;
    }
    else if($('#hdn_cert_stage_id').val().toString()=="2" & $('#TxtCourierNumber').val()=='')
    {
        alert("Please enter courier number.");
        return false;
    }
    else if($('#hdn_cert_stage_id').val().toString()=="3" & $('#TxtReceivedDate').val()=='')
    {
        alert("Please enter received date.");
        return false;
    }
    else if($('#hdn_cert_stage_id').val().toString()=="4" & $('#TxtPlannedDistributionDate').val()=='')
    {
        alert("Please enter planned dstribution date.");
        return false;
    }
    else if($('#hdn_cert_stage_id').val().toString()=="5" & $('#TxtActualDistributionDate').val()=='')
    {
        alert("Please enter actual dstribution date.");
        return false;
    }
    var URL=$('#hdn_web_url').val()+ "/ChangeCertificationStage";
        $.ajax({
            type:"POST",
            url:URL,
            data:{
                "batch_id" : $('#hdn_batch_id').val(),
                "batch_code" : $('#hdn_batch_code').val(),
                "user_id" : $('#hdn_home_user_id').val(),
                "current_stage_id" : $('#hdn_cert_stage_id').val(),
                "enrollment_ids" : cands,
                "sent_printing_date" : $('#TxtSentPrintingDate').val(),
                "sent_center_date" : $('#TxtSentCenterDate').val(),
                "expected_arrival_date" : $('#TxtCenterExpArrivalDate').val(),
                "received_date" : $('#TxtReceivedDate').val(),
                "planned_distribution_date" : $('#TxtPlannedDistributionDate').val(),
                "actual_distribution_date" : $('#TxtActualDistributionDate').val(),               
                "cg_name" :  $('#TxtCGName').val(),
                "cg_desig" :  $('#TxtCGDesig').val(),
                "cg_org" :  $('#TxtCGOrg').val(),
                "cg_org_loc": $('#TxtCGOrgLoc').val(),
                "remark" : $('#TxtRemark').val(),
                "courier_number" : $('#TxtCourierNumber').val(),
                "courier_name" : $('#TxtCourierName').val(),
                "courier_url" : $('#TxtCourierUrl').val()
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
                                window.location.href = '/certification';
                                
                            }); 
            },
            error:function(x){
                alert('error');
            }
        });

}
function Back()
{
    window.location.href = '/certification';

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
function UploadCandCertificate(Enrollment_Id)
{
    $('#hdn_cand_enrol_id').val(Enrollment_Id);
    $('#tr_candidate_detail').modal('hide');
    $('#mdl_candidate_certificate_upload').modal('show');


}
function UploadCandImage(Enrollment_Id)
{
    $('#hdn_cand_enrol_id').val(Enrollment_Id);
    $('#tr_candidate_detail').modal('hide');
    $('#mdl_candidate_cand_image_upload').modal('show');


}

function UploadBatchImage(batch_id,batch_code)
{
    $('#hdn_batch_id').val(batch_id);
    $('#hdn_batch_code').val(batch_code);
    $('#mdl_candidate_batch_image_upload').modal('show');
}
function UploadCandidatecertificateFileData()
{  
 
    
    
    if ($('#fileCertificate').get(0).files.length === 0) {
        alert("No files selected.");
        return;
    }
    else
    {
//        UploadFileToProcess();
//    }
//}
        var fileExtension = ['xlsx','jpg','png','pdf','doc','docx','jpeg','csv']
        if ($.inArray($('#fileCertificate').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            $("#imgSpinnerCerti").show();

            var files=document.getElementById("fileCertificate").files;
            var file=files[0];
            var file_name= $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name;
            $('#hdn_certi_file_name').val(file_name);
            var file_path=$('#hdn_AWS_S3_path').val()+"certification/certificate_copy/" + file_name;
            var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET",api_url );
                xhr.onreadystatechange = function(){
                    if(xhr.readyState === 4){
                    if(xhr.status === 200){
                        var response = JSON.parse(xhr.responseText);
                        //console.log(response);
                        uploadCertificateFileToS3(file, response.data, response.url);
                        $("#imgSpinnerCerti").hide();
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

function uploadCertificateFileToS3(file, s3Data, url){
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
            UploadCertificateFileToProcess();
        }
        else{
            alert("Could not upload file to s3.");
        }
    }
    };
    xhr.send(postData);
}

function UploadCertificateFileToProcess()
{
       
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_assessment_certificate_copy",
        data:{
            "file_name":$('#hdn_certi_file_name').val(),
            "user_id" : $('#hdn_home_user_id').val(),
            "enrollment_id" : $('#hdn_cand_enrol_id').val(),
            "batch_id" : $('#hdn_batch_id').val()
           
        },
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
                            $('#fileCertificate').val("");
                            $('#mdl_candidate_certificate_upload').modal('hide');
                            GetPassedCandidates($('#hdn_batch_id').val(),parseInt($('#hdn_cert_stage_id').val()),$('#hdn_batch_code').val());
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
                    window.location.href = '/certification';
                }); 
           
        }
    });
}
function UploadBulkcertificateFileData()
{  
    var enrollments='';
    $('[name=candcheckcase]').each(function () {
        if($(this).prop('checked') == true)
        {
            enrollments+= $(this).val()+',';
        }
        
    });
    enrollments=enrollments.substring(0,enrollments.length-1)
    var cands=enrollments.toString();
    //alert(cands);
    //cands=cands.substring(0,cands.length-1)
    $("#hdn_enrol_ids").val(cands);
    if ((cands.toString().length)==0)
    {
        alert('Please select candidates:')
        $("#imgSpinnerBulkCerti").hide();
    }
    
    else if ($('#BulkCertificateFile').get(0).files.length === 0) {
        alert("No files selected.");
        return;
    }
    else
    {
        var fileExtension = ['xlsx','jpg','png','pdf','doc','docx','jpeg','csv']
        if ($.inArray($('#BulkCertificateFile').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            $("#imgSpinnerBulkCerti").show();

            var files=document.getElementById("BulkCertificateFile").files;
            var file=files[0];
            var file_name= $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name;
            $('#hdn_bulk_certi_file_name').val(file_name);
            var file_path=$('#hdn_AWS_S3_path').val()+"certification/certificate_copy/" + file_name;
            var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET",api_url );
                xhr.onreadystatechange = function(){
                    if(xhr.readyState === 4){
                    if(xhr.status === 200){
                        var response = JSON.parse(xhr.responseText);
                        //console.log(response);
                        uploadBulkCertificateFileToS3(file, response.data, response.url);
                        $("#imgSpinnerBulkCerti").hide();
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

function uploadBulkCertificateFileToS3(file, s3Data, url){
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
            UploadBulkCertificateFileToProcess();
        }
        else{
            alert("Could not upload file to s3.");
        }
    }
    };
    xhr.send(postData);
}

function UploadBulkCertificateFileToProcess()
{
       
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_assessment_certificate_copy_bulk_upload",
        data:{
            "file_name":$('#hdn_bulk_certi_file_name').val(),
            "user_id" : $('#hdn_home_user_id').val(),
            "enrollment_id" : $('#hdn_enrol_ids').val(),
            "batch_id" : $('#hdn_batch_id').val()
           
        },
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
                            window.location.href = '/certification';
                            //$('#mdl_bulk_certificate_upload').modal('hide');
                            //GetPassedCandidates($('#hdn_batch_id').val(),parseInt($('#hdn_cert_stage_id').val()),$('#hdn_batch_code').val());
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
                    window.location.href = '/certification';
                }); 
           
        }
    });
}

function BulkDowloadCertificate(){
    var URL=$('#hdn_web_url').val()+ "/AllCertificateNames"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "batch_id": $('#hdn_batch_id').val()    ,
            "stage": $('#hdn_cert_stage_id').val()        
        },

        success: function (data){
            if(data.Certificates != null)
            {
                var count=data.Certificates.length;
                if( count> 0)
                {
                  
                   for(var i=0;i<count;i++)
                   {
                        DownloadCertificate(data.Certificates[i].Certificate_Name)
                   }
                       
                }
                else{
                    alert("No Files to Download!");
                }
               
            }
        },
        error:function(err)
        {
            alert('Error while downloading certificates! Please try again');
            return false;
        }
    });
    return false;
}
function UploadCandidateImageFileData()
{  
 
    
    
    if ($('#fileCandImage').get(0).files.length === 0) {
        alert("No files selected.");
        return;
    }
    else
    {
//        UploadFileToProcess();
//    }
//}
        var fileExtension = ['xlsx','jpg','png','pdf','doc','docx','jpeg','csv']
        if ($.inArray($('#fileCandImage').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            $("#imgSpinnerCandImage").show();

            var files=document.getElementById("fileCandImage").files;
            var file=files[0];
            var file_name= $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name;
            $('#hdn_cand_image_file_name').val(file_name);
            var file_path=$('#hdn_AWS_S3_path').val()+"certification/batch_candidate_images/" + file_name;
            var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET",api_url );
                xhr.onreadystatechange = function(){
                    if(xhr.readyState === 4){
                    if(xhr.status === 200){
                        var response = JSON.parse(xhr.responseText);
                        //console.log(response);
                        uploadCandImageFileToS3(file, response.data, response.url);
                        $("#imgSpinnerCandImage").hide();
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

function uploadCandImageFileToS3(file, s3Data, url){
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
            UploadCandImageFileToProcess();
        }
        else{
            alert("Could not upload file to s3.");
        }
    }
    };
    xhr.send(postData);
}

function UploadCandImageFileToProcess()
{
       
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_cerification_cand_image",
        data:{
            "file_name":$('#hdn_cand_image_file_name').val(),
            "user_id" : $('#hdn_home_user_id').val(),
            "enrollment_id" : $('#hdn_cand_enrol_id').val(),
            "batch_id" : $('#hdn_batch_id').val()
           
        },
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
                            $('#fileCandImage').val("");
                            $('#mdl_candidate_cand_image_upload').modal('hide');
                            GetPassedCandidates($('#hdn_batch_id').val(),5,$('#hdn_batch_code').val());
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
                    window.location.href = '/certification';
                }); 
           
        }
    });
}
function UploadBatchImageFileData()
{  
 
    
    
    if ($('#fileBatchImage').get(0).files.length === 0) {
        alert("No files selected.");
        return;
    }
    else
    {
//        UploadFileToProcess();
//    }
//}
        var fileExtension = ['xlsx','jpg','png','pdf','doc','docx','jpeg','csv']
        if ($.inArray($('#fileBatchImage').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            $("#imgSpinnerBatchImage").show();

            var files=document.getElementById("fileBatchImage").files;
            var file=files[0];
            var file_name= $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name;
            $('#hdn_batch_image_file_name').val(file_name);
            var file_path=$('#hdn_AWS_S3_path').val()+"certification/batch_candidate_images/" + file_name;
            var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET",api_url );
                xhr.onreadystatechange = function(){
                    if(xhr.readyState === 4){
                    if(xhr.status === 200){
                        var response = JSON.parse(xhr.responseText);
                        //console.log(response);
                        uploadBatchImageFileToS3(file, response.data, response.url);
                        $("#imgSpinnerBatchImage").hide();
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

function uploadBatchImageFileToS3(file, s3Data, url){
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
            UploadBatchImageFileToProcess();
        }
        else{
            alert("Could not upload file to s3.");
        }
    }
    };
    xhr.send(postData);
}

function UploadBatchImageFileToProcess()
{
       
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_cerification_batch_image",
        data:{
            "file_name":$('#hdn_batch_image_file_name').val(),
            "user_id" : $('#hdn_home_user_id').val(),
            "batch_id" : $('#hdn_batch_id').val()
           
        },
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
                           Back();
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
                    window.location.href = '/certification';
                }); 
           
        }
    });
}

function DownloadCertificate(image_name)
{   
    var file_path=$('#hdn_AWS_S3_path').val()+"certification/certificate_copy/" + image_name;    
    var api_url=$('#hdn_COL_url').val() + "s3_signed_url_for_file?file_path="+file_path+"&file_name="+image_name;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", api_url);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
        if(xhr.status === 200){
            //var response = JSON.parse(xhr.responseText);
            var url=xhr.responseText;
            console.log(url);
            var xhr_down = new XMLHttpRequest();
            xhr_down.open("GET",url );
            xhr_down.responseType = "blob";

            xhr_down.onload = function () {
                saveData(this.response,image_name ); // saveAs is now your function
            };
            xhr_down.send();
        }
        else{
            alert("Could not get signed URL.");
        }
        }
    };
    xhr.send();
    
}
function DownloadCertificationImage(image_name)
{
    //alert(image_name);
    var file_path=$('#hdn_AWS_S3_path').val()+"certification/batch_candidate_images/" + image_name;    
    var api_url=$('#hdn_COL_url').val() + "s3_signed_url_for_file?file_path="+file_path+"&file_name="+image_name;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", api_url);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
        if(xhr.status === 200){
            //var response = JSON.parse(xhr.responseText);
            var url=xhr.responseText;
            console.log(url);
            var xhr_down = new XMLHttpRequest();
            xhr_down.open("GET",url );
            xhr_down.responseType = "blob";

            xhr_down.onload = function () {
                saveData(this.response,image_name ); // saveAs is now your function
            };
            xhr_down.send();
        }
        else{
            alert("Could not get signed URL.");
        }
        }
    };
    xhr.send();
}
function saveData(blob, fileName) // does the same as FileSaver.js
{

    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";

    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);
}


