
var varTable;
var filter_role_id;
/*
function LoadRM_Role_ddl(){
    var URL=$('#hdn_web_url').val()+ "/All_RM_role"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.RM_ROLE != null)
            {
                $('#ddlRM_role').empty();
                var count=data.RM_ROLE.length;
                if( count> 0)
                {
                    $('#ddlRM_role').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRM_role').append(new Option(data.RM_ROLE[i].User_Role_Name,data.RM_ROLE[i].User_Role_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlRM_role').append(new Option('ALL','-1'));
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


//LoadClusterddl
*/
function LoadR_Manager_ddl(){
    var URL=$('#hdn_web_url').val()+ "/All_Reporting_manager_basedon_role_id"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,       
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json", 
        data:{
            "rm_role_id" : ''//$('#ddlRM_role').val().toString()//$('#ddlProject option:selected').val()
        },
		success: function (data){
            if(data.Users != null)
            {
                $('#ddl_R_Manager').empty();
                var count=data.Users.length;
                if( count> 0)
                {
                    //$('#ddl_R_Manager').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddl_R_Manager').append(new Option(data.Users[i].User_Name,data.Users[i].User_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddl_R_Manager').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Cluster! Please try again');
            return false;
        }
    });
    return false;
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

function Loadentityddl(){
    var URL=$('#hdn_web_url').val()+ "/All_entity"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Entity != null)
            {
                $('#ddlentity').empty();
                var count=data.Entity.length;
                if( count> 0)
                {
                    //$('#ddlentity').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlentity').append(new Option(data.Entity[i].Entity_Name,data.Entity[i].Entity_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlentity').append(new Option('ALL','-1'));
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
function LoadProjectddl(){
    
    var URL=$('#hdn_web_url').val()+ "/AllProjectList"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Project != null)
            {
                $('#ddl_Project').empty();
                var count=data.Project.length;
                if( count> 0)
                {
                    //$('#ddl_Project').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddl_Project').append(new Option(data.Project[i].Project_Name,data.Project[i].Project_Id));
                    //$('#ddlentity').val('-1');
                }
                else
                {
                    $('#ddl_Project').append(new Option('ALL','-1'));
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
function LoadStatusddl(){
    var URL=$('#hdn_web_url').val()+ "/All_Emp_Status"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.emp_status != null)
            {
                $('#ddl_status').empty();
                var count=data.emp_status.length;
                if( count> 0)
                {
                    //$('#ddl_status').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddl_status').append(new Option(data.emp_status[i].Employment_Status_Name,data.emp_status[i].Employment_Status_Id));
                    //$('#ddlentity').val('-1');
                }
                else
                {
                    $('#ddl_status').append(new Option('ALL','-1'));
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

function LoadRoleddl(){
    var URL=$('#hdn_web_url').val()+ "/All_role"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Role != null)
            {
                $('#ddlRole').empty();
                var count=data.Role.length;
                if( count> 0)
                {
                    //$('#ddlRole').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRole').append(new Option(data.Role[i].Employee_Role_Name,data.Role[i].Employee_Role_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlRole').append(new Option('ALL','-1'));
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
function LoadNEORoleddl(needed){
    var URL=$('#hdn_web_url').val()+ "/All_role_neo"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Role != null)
            {
                $('#ddlNeoRole').empty();
                $('#ddlJobsRole').empty();
                $('#ddlCRMRole').empty();
                var count=data.Role.length;
                if( count> 0) 
                {
                    //$('#ddlRole').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                    {
                        $('#ddlNeoRole').append(new Option(data.Role[i].User_Role_Name,data.Role[i].User_Role_Id));
                        $('#ddlJobsRole').append(new Option(data.Role[i].User_Role_Name,data.Role[i].User_Role_Id));
                        $('#ddlCRMRole').append(new Option(data.Role[i].User_Role_Name,data.Role[i].User_Role_Id));
                        
                    }
                    if(needed!='' && needed!='0' && needed!=null)
                            {
                                //console.log(needed);
                                $('#ddlNeoRole').val(needed.split(',')); 
                            }
                        
                        //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlNeoRole').append(new Option('ALL','-1'));
                    $('#ddlJobsRole').append(new Option('ALL','-1'));
                    $('#ddlCRMRole').append(new Option('ALL','-1'));

                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Neo User Roles! Please try again');
            return false;
        }
    });
    return false;
}
function LoadDEPTddl(){
    var URL=$('#hdn_web_url').val()+ "/All_dept"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Dept != null)
            {
                $('#ddlDEPT').empty();
                var count=data.Dept.length;
                if( count> 0)
                {
                    //$('#ddlDEPT').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlDEPT').append(new Option(data.Dept[i].Employee_Department_Name,data.Dept[i].Employee_Department_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlDEPT').append(new Option('ALL','-1'));
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


function LoadTable(FilterRoleId)
{       //alert($('#ddlDEPT').val().toString() +'\n'+$('#ddlRole').val().toString()+'\n'+$('#ddlentity').val().toString() +'\n'+$('#ddlRegion').val().toString()+'\n'+$('#ddlRM_role').val().toString()+'\n'+$('#ddl_R_Manager').val().toString())
    filter_role_id=FilterRoleId;
        vartable1 = $("#tbl_users").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/user_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id = $('#hdn_home_user_id').val();
                d.entity_ids = $('#ddlentity').val().toString();
                d.dept_ids = $('#ddlDEPT').val().toString();
                d.role_ids = $('#ddlRole').val().toString();                
                d.region_ids = $('#ddlRegion').val().toString();
                d.RM_Role_ids = '';//$('#ddlRM_role').val().toString();
                d.project_ids=$('#ddl_Project').val().toString();
                d.R_mangager_ids = $('#ddl_R_Manager').val().toString();
                d.status_ids=$('#ddl_status').val().toString();
                d.filter_role_id=filter_role_id;
                d.user_region_id = $('#hdn_user_region_id').val();
                d.user_role_id = $('#hdn_home_user_role_id').val();
            },
            error: function (e) {
                $("#tbl_users tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id == 1 )
                {
                    varButtons += '<a onclick="EditUserDetail(\'' + row.User_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User Roles" class="fas fa-edit" ></i></a>';
                }
                     return varButtons;
                }
            },

            { 
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if((row.User_Role_Id!='2'&&row.User_Role_Id!='24')||$('#hdn_home_user_role_id').val()!='1')
                        varButtons=row.User_Name;
                    else
                    {
                        varButtons += '<a onclick="Getusertarget(\'' + row.User_Id + '\',\'' + row.User_Name + '\')" style="color:blue;cursor:pointer" >' + row.User_Name + '</a>';
                    }                    
                    return varButtons;
                }
            },
            //{ "data": "User_Name" },
            { "data": "Email" },
            { "data": "Employee_Code" },            
            { "data": "Entity_Name" },
            { "data": "Department_Name" },
            { "data": "Employee_Role_Name" },
            { "data": "User_Role_Name" },
            { "data": "Jobs_Role_Name" },
            { "data": "Crm_Role_Name" },
            { "data": "Region" },
            { 
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Project==0)
                        varButtons=row.Project;
                    else
                    {
                        varButtons += '<a onclick="GetProjectDetails(\'' + row.User_Id + '\',\'' + row.User_Name + '\')"  style="color:blue;cursor:pointer" >' + row.Project + '</a>';
                    }                    
                    return varButtons;
                }
            },
            { "data": "Reporting_Manager_Name"},
            { "data": "Employment_Status"},
            { "visible":false, "data": "Center_Name" },
            { "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            }
        ],
        drawCallback: function(){
            $('#tbl_users_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}

function EditUserDetail(UserId)
{
    $('#hdn_neo_user_id').val(UserId);
    //LoadNEORoleddl(needed);
    $('.dropdown-search-filter').select2({
        width: '100%' 
    });
    var URL=$('#hdn_web_url').val()+ "/get_user_role_details_new?user_id="+UserId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){

                $('#TxtEmpCode').val(data.UserDetail.Employee_Code);
                $('#TxtEmpName').val(data.UserDetail.Employee_Name);              
                LoadNEORoleddl(data.UserDetail.Neo_Role_Id);
                $('#ddlJobsRole').val(data.UserDetail.Jobs_Role_Id);
                $('#ddlCRMRole').val(data.UserDetail.Crm_Role_Id);
                if(data.UserDetail.Is_Active)
                    $('#isactive').prop('checked',true);
                else
                    $('#isactive').prop('checked',false);  
            },
            error:function(err)
            {
                alert('Error! Please try again');
                return false;
            }
        });
     
    $('#mdl_add_edit_role').modal('show');
    
}
function UpdateRole()
{

    var URL=$('#hdn_web_url').val()+ "/tag_user_roles";
        $.ajax({
            type:"POST",
            url:URL,
            data:{
                "login_user_id": $('#hdn_home_user_id').val() ,
                "user_id": $('#hdn_neo_user_id').val(),
                "neo_role":($('#ddlNeoRole').val()==null? '20':$('#ddlNeoRole').val().toString()),
                "jobs_role":($('#ddlJobsRole').val()==null? '20':$('#ddlJobsRole').val().toString()),
                "crm_role":($('#ddlCRMRole').val()==null? '20':$('#ddlCRMRole').val().toString()),
                "isactive" : $('#isactive').prop('checked')
            },
            success:function(data){
                if(data.PopupMessage.message =="Success")
                {
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+"!!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/user';                          
                        });

                }
                else{
                    swal({   
                        title:data.PopupMessage.message,
                        text:"Error in updating Roles!",
                        icon:"error",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/user';                          
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

function uploadEmployeeAllocation()
{
    $('#HduploadFileEmp').text('Upload Employee Allocation Plan');
    $('#imgSpinner2').hide();
    $('#mdl_employee_allocation_upload').modal('show');
    
    $('#myFileemp').val('');
}


function DownloadEmployeeTimeTemplate(){
    //var date = $('#Month_Year').val()+'-01';
    //console.log(date);
    if(1==0){
        alert('please search date');
        return 
    }
    else{
        $("#imgSpinner2").show();
        var URL=$('#hdn_web_url').val()+ "/DownloadEmpTimeAllocationTemplate"
        $.ajax({
            type: "POST",
            dataType: "json",
            url: URL,
            data: {
                'user_id':$('#hdn_home_user_id').val(),
                'user_role_id':$('#hdn_home_user_role_id').val()
            },
            success: function(resp) 
            {
                console.log(resp)
                if (resp.Status){
                    var varAnchor = document.getElementById('lnkDownload');
                    varAnchor.href = $('#hdn_web_url').val() + '/report file/' + resp.filename;
                    $("#imgSpinner2").hide();
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
                    alert(resp.Description)
                    $("#imgSpinner2").hide();
                    
                }
            },
            error:function()
            {
                //console.log(resp)
                $("#imgSpinner2").hide();
            }
        });
    }
 
}

function UploadUserSubProjectAlloctaionFile(){
    if ($('#myFileemp').get(0).files.length === 0) {
        alert("No files selected.");
    }
    else
    {
        var fileExtension = ['xlsx']
        if ($.inArray($('#myFileemp').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {          
            $("#imgSpinner3").show();
            var files=document.getElementById("myFileemp").files;
            var file=files[0];
            var status;
            /*status = UploadFileData(file);
            if(status==0){
                alert('not able to upload to s3');
                return;
            }*/
        }
        
        var form_data = new FormData($('#formAllocationUpload')[0]);
        form_data.append('user_id',$('#hdn_home_user_id').val());
        form_data.append('user_role_id',$('#hdn_home_user_role_id').val());
        $.ajax({
            type: 'POST',
            url: $('#hdn_web_url').val()+ "/upload_employee_allocation_plan",
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
                    if (data.message=="Validation_Error"){
                        message=data.error;
                        title="Error";
                        icon="error";
                    }
                    else {
                        message=data.message;
                        title="Error";
                        icon="error";
                    }
                }
                var span = document.createElement("span");
                span.innerHTML = message;
                swal({   
                            title:title,
                            content: span,
                            //text:message,
                            icon:icon,
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/user';
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
                        window.location.href = '/user';
                });
            }
        });        
    }
}

function GetProjectDetails(User_Id,User_Name)
{
    $('#hdn_upl_user_id').val(User_Id);
    $('#hdn_upl_user_name').val(User_Name);
    var URL=$('#hdn_web_url').val()+ "/GetSubProjectsForUser?user_id="+User_Id;
    $.ajax({
        type:"GET",
        url:URL,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tblSubProject").dataTable().fnDestroy();
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
                            varHtml+='  <td style="text-align:center;">'+ User_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Sub_Project_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Sub_Project_Name +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Project_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Project_Name +'</td>';  
                            varHtml+='  <td style="text-align:center;">'+ data.SubProjects[i].Bu +'</td>';  
                            //varHtml+='  <td style="text-align:center;">2h20m</td>';         
                                   
                            varHtml+='</tr>';
                            
                        }
                            $("#tblSubProject tbody").append(varHtml);
                            $("#tblSubProject").DataTable();
                            $('#divSubProjectList').modal('show');
                            varHtml='';
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

function Getusertarget(UserId,UserName)
    {
        $('#hdn_modal_user_id').val(UserId);
        $('#headertarget').text(UserName);

        var URL=$('#hdn_web_url').val()+ "/GetUserTargets?user_id="+UserId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                $("#tbl_target").dataTable().fnDestroy();
                $("#tbl_target tbody").empty();
                if(!jQuery.isEmptyObject(data))
                {   if (data.UserTarget != null){
                        count=data.UserTarget.length;
                        if (count>0)
                        {   varHtml='';
                            //console.log(data.CenterRooms[0].Course_Ids);
                            for(var i=0;i<count;i++)
                            {
                                td_open= '  <td style="text-align:center;">' ;
                                td_close=   '</td>';       
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].S_No +'</td>';
                                varHtml+='  <td style="text-align:center;">'+'<a onclick="EditModal(\'' + data.UserTarget[i].From_Date_Form + '\',\'' + data.UserTarget[i].To_Date_Form + '\',\'' +  data.UserTarget[i].Product + '\',\'' + data.UserTarget[i].Target + '\',\'' + data.UserTarget[i].User_Id + '\',\'' + data.UserTarget[i].Is_Active + '\',\'' + data.UserTarget[i].User_Target_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Monthly Target" class="fas fa-edit" ></i></a>'+'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].From_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].To_Date +'</td>'; 
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].Product_Name +'</td>';                   
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].Target +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].User_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].Created_On +'</td>';
                                varHtml+='</tr>';                            
                            }
                            $("#tbl_target tbody").append(varHtml);
                                $("#tbl_target").DataTable({
                                drawCallback: function(){
                                    $('#tbl_target_paginate ul.pagination').addClass("pagination-rounded");
                                }
                            });
                                $('#mdl_user_target').modal('show');
                                varHtml='';
                        }
                        else
                        {
                            //varHtml='<tr><td colspan="4" style="text-align:center;">No records found</td></tr>'                            
                            //$("#tbl_users tbody").append(varHtml);
                            $("#tbl_target").DataTable();
                            $('#mdl_user_target').modal('show');
                        } 
                        
                    }
                }
                else
                {
                    //varHtml='<tr><td colspan="4" style="text-align:center;">No records found</td></tr>'
                    //$("#tbl_users tbody").append(varHtml);
                    $("#tbl_target").DataTable();
                    $('#mdl_user_target').modal('show');
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

    function AddModal()
    {   
        $('#isactive').prop('checked',true);
        $('#From_Date').val('');
        $('#To_Date').val('');
        $('#ddlproduct').val('1');
        $('#target').val('');
        $('#hdn_user_target_id').val("0");
        $('#hdn_user_id_m2').val($('#hdn_modal_user_id').val()); 
        
        $('#mdl_user_target').modal('hide');
        $('#mdl_add_edit_targets').modal('show');
    }
    
    function EditModal(From_Date, To_Date, Product, Target, User_Id, Is_Active, User_Target_Id)
    {   
        if(Is_Active)
            $('#isactive').prop('checked',true);
        else 
            $('#isactive').prop('checked',false);
        $('#From_Date').val(From_Date);
        $('#To_Date').val(To_Date);
        $('#ddlproduct').val(Product);
        $('#target').val(Target);
        $('#hdn_user_target_id').val(User_Target_Id);
        $('#hdn_user_id_m2').val($('#hdn_modal_user_id').val()); 
        $('#mdl_user_target').modal('hide');
        $('#mdl_add_edit_targets').modal('show');
        
    }
    function AddeEdittUserTarget()
    {   //alert($('#hdn_user_id_m2').val())
        var from_date = new Date($('#From_Date').val())
        from_date = moment(from_date).format('YYYY/MM/DD');
        //alert(from_date);
        var to_date = new Date($('#To_Date').val())
        to_date = new Date(to_date.getFullYear(), to_date.getMonth() + 1, 0);
        to_date = moment(to_date).format('YYYY/MM/DD');
        //alert(to_date);

        if (from_date>to_date){
            alert('Please select valid month-year')
        }
        else{
            var URL=$('#hdn_web_url').val()+ "/AddeEdittUserTarget";
        $.ajax({
            type:"POST",
            url:URL,
            data:{
                "From_Date" : from_date,
                "To_Date" : to_date,
                "target" : $('#target').val(),
                "isactive" : $('#isactive').prop('checked'),
                "user_id":$('#hdn_user_id_m2').val(),
                "user_target_id":$('#hdn_user_target_id').val(),
                "product":$('#ddlproduct').val()
            },
            success:function(data){
                var message="",title="",icon="";
                if(data.PopupMessage.status){
                    message=data.PopupMessage.message;
                    title="Success";
                    icon="success";
                }
                else{
                    message=data.PopupMessage.message;
                    title="Error";
                    icon="error";
                }
                swal({   
                            title:title,
                            text:message,
                            icon:icon,
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/user';
                                // $('#mdl_add_edit_Users').modal('hide');
                                // LoadTable();
                            }); 
            },
            error:function(x){
                alert('error');
            }
        });
        }
    }

    function UploadUserMdl()
    {
        
        $('#HduploadFile').text('Upload User Details:');
        $('#imgSpinner1').hide();
        $('#mdl_upload_user_plan').modal('show');
        $('#myFile').val('');
    }
    function DownloadUserTemplate()
    {
        window.location='/Bulk Upload/'+'User_Add_Edit_Template.xlsx';
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
    
                var file_path=$('#hdn_AWS_S3_path').val()+"bulk_upload/employee/" + $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name; 
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
        var form_data = new FormData($('#formUpload')[0]);
        form_data.append('user_id',$('#hdn_home_user_id').val());
        form_data.append('user_role_id',$('#hdn_home_user_role_id').val());
        $.ajax({
            type: 'POST',
            url: $('#hdn_web_url').val()+ "/upload_user",
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
                    if (data.message=="Validation_Error"){
                        message=data.error;
                        title="Error";
                        icon="error";
                    }
                    else {
                        message=data.message;
                        title="Error";
                        icon="error";
                    }
                }
                var span = document.createElement("span");
                span.innerHTML = message;
                swal({   
                            title:title,
                            content: span,
                            //text:message,
                            icon:icon,
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                window.location.href = '/user';
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
                        window.location.href = '/user';
                    }); 
                
            }
        });
    }

    function DownloadTableBasedOnSearch()
{                   
    $("#imgSpinner").show();
    // from candidate
    if(0==1)
        {
            
            $("#imgSpinner").hide();
        }
    else{
        var URL=$('#hdn_web_url').val()+ "/download_users_list"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                        
                        "user_id":$('#hdn_home_user_id').val(),
                        "user_role_id":$('#hdn_home_user_role_id').val(),
                        "user_region_id":$('#hdn_user_region_id').val(),
                        "entity_ids":$('#ddlentity').val().toString(),
                        "dept_ids":$('#ddlDEPT').val().toString(),
                        "role_ids":$('#ddlRole').val().toString(),
                        "region_ids":$('#ddlRegion').val().toString(),
                        "RM_Role_ids":'',
                        "project_ids":$('#ddl_Project').val().toString() ,     
                        "R_mangager_ids":$('#ddl_R_Manager').val().toString(),
                        "status_ids":$('#ddl_status').val().toString(),
                        "filter_role_id":filter_role_id               
                    },
                    success:function(data){
                        if(data!=null)
                        {         
                            if(data.success)
                            {
                                $("#imgSpinner").hide();        
                                window.location=data.FilePath+data.FileName;
                            }    
                            else
                            {
                                $("#imgSpinner").hide(); 
                                alert(data.msg);
                                return false;
                            }  
                        }                    
                    },
                    error:function()
                    {
                        //$("#imgSpinner").hide();
                    }
                });
        
    }
}