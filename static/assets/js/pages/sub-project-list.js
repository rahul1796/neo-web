var varTable;
function LoadEntitydl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Entity"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Entity != null)
            {
                $('#ddlEntity').empty();
                var count=data.Entity.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlEntity').append(new Option(data.Entity[i].Entity_Name,data.Entity[i].Entity_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlEntity').append(new Option('No Entity','-1'));
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
function LoadCustomerdl(){
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
                $('#ddlCustomer').empty();
                var count=data.Clients.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCustomer').append(new Option(data.Clients[i].Customer_Name,data.Clients[i].Customer_Id));
                    //$('#ddlCourse').val('-1');
                    if(CustomerId!='0')
                    {
                        $('#ddlCustomer').val(CustomerId);
                        LoadProject();
                    }
                }
                else
                {
                   // $('#ddlCustomer').append(new Option('No Customer','-1'));
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
function LoadProjectGroupdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Project_Group"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Project_Group != null)
            {
                $('#ddlP_Group').empty();
                var count=data.Project_Group.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlP_Group').append(new Option(data.Project_Group[i].Project_Group_Name,data.Project_Group[i].Project_Group_Id));
                    //$('#ddlCourse').val('-1');
                }	
                else
                {
                    $('#ddlP_Group').append(new Option('No Project Group','-1'));
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
function LoadBlockdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Block"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Block != null)
            {
                $('#ddlBlock').empty();
                var count=data.Block.length;
                if( count> 0)
                {
                    
                    for(var i=0;i<count;i++)
                        $('#ddlBlock').append(new Option(data.Block[i].Block_Name,data.Block[i].Block_Id));
                    
                }	
                else
                {
                    $('#ddlBlock').append(new Option('No Block','-1'));
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
function LoadPracticedl(){
    var URL=$('#hdn_web_url').val()+ "/AllPracticeList"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Pratices != null)
            {
                $('#ddlPractice').empty();
                var count=data.Pratices.length;
                if( count> 0)
                {
                    
                    for(var i=0;i<count;i++)
                        $('#ddlPractice').append(new Option(data.Pratices[i].Practice_Name,data.Pratices[i].Practice_Id));
                    
                }	
                else
                {
                    $('#ddlPractice').append(new Option('No Practice','-1'));
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
function LoadBUdl(){
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
                    
                    for(var i=0;i<count;i++)
                        $('#ddlBU').append(new Option(data.BU[i].Bu_Name,data.BU[i].Bu_Id));
                    
                }	
                else  	
                {
                    $('#ddlBU').append(new Option('No BU','-1'));
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
function LoadProductdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Product"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Product != null)
            {
                $('#ddlProduct').empty();
                var count=data.Product.length;
                if( count> 0)
                {
                    
                    for(var i=0;i<count;i++)
                        $('#ddlProduct').append(new Option(data.Product[i].Product_Name,data.Product[i].Product_Id));                    
                }	
                else  		
                {
                    $('#ddlProduct').append(new Option('No Product','-1'));
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

function LoadProject(){
    var URL=$('#hdn_web_url').val()+ "/GetALLProject_multiple"  //"/GetALLProject_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ClientId":$('#ddlCustomer').val().toString(),
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
                    if(ProjectId!='0') 
                        $('#ddlProject').val(ProjectId);
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
function LoadUsers(){
    $('#trainer_type').css('display', 'none');
    if($('#ddlUserRole').val()== 7)
    {
        //$('#trainer_type').visible = true;
        $('#trainer_type').css('display', 'block');
        LoadTrainerType();
        return;
    }    
    
    var URL=$('#hdn_web_url').val()+ "/GetUsersBasedOnRole?user_role_id="+$('#ddlUserRole').val()  
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
                $('#ddlUsers').empty();
                var count=data.Users.length;
                if( count> 0)
                {
                     for(var i=0;i<count;i++)
                        $('#ddlUsers').append(new Option(data.Users[i].User_Name,data.Users[i].User_Id));
                   
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
function LoadTrainerType(){
    $('#ddlTrainerType').empty();
    $('#ddlTrainerType').append(new Option("All Trainers",0));
    $('#ddlTrainerType').append(new Option("Internal Trainers",1));
    $('#ddlTrainerType').append(new Option("External Trainers",2));
    LoadTrainers()
}
function LoadTrainers(){
    
    var URL=$('#hdn_web_url').val()+ "/GetTrainersBasedOnType?trainer_flag="+$('#ddlTrainerType').val()
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
                $('#ddlUsers').empty();
                var count=data.Users.length;
                if( count> 0)
                {
                     for(var i=0;i<count;i++)
                        $('#ddlUsers').append(new Option(data.Users[i].User_Name,data.Users[i].User_Id));
                   
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

function LoadTable()
{
    vartable1 = $("#tbl_projects").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        //"scrollX": true,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/sub_project_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.entity = $('#ddlEntity').val().toString();
                d.customer  = $('#ddlCustomer').val().toString();
                d.p_group   = $('#ddlP_Group').val().toString();
                d.block     = $('#ddlBlock').val().toString();
                d.practice  = $('#ddlPractice').val().toString();
                d.bu        = $('#ddlBU').val().toString();
                d.product   = $('#ddlProduct').val().toString();
                d.status    = $('#ddlStatus').val().toString();
                d.project   =$('#ddlProject').val().toString();
                d.user_id =$('#hdn_home_user_id').val();
                d.user_role_id = $('#hdn_home_user_role_id').val();
                d.user_region_id=$('#hdn_user_region_id').val();
            },
            error: function (e) {
                $("#tbl_projects tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },
        "columns": [
            { "data": "S_No"},
            {"visible": ($('#hdn_home_user_role_id').val()=='1'||$('#hdn_home_user_role_id').val()=='15')?true:false,
            
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditsubProjectDetail(\'' + row.Sub_Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Sub Project" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Sub_Project_Code"},
            { "data": "Sub_Project_Name"},
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Center_Count=="")
                    varButtons=row.Center_Count;
                else
                {
                    varButtons += '<a onclick="GetCenters(\'' + row.Sub_Project_Id + '\',\''+row.Sub_Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Center_Count + '</a>';
                }
                
                return varButtons;
                }
            },
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Course_Count=="")
                    varButtons=row.Course_Count;
                else
                {
                    varButtons += '<a onclick="GetCourses(\'' + row.Sub_Project_Id + '\',\''+row.Sub_Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Course_Count + '</a>';
                }
                
                return varButtons;
                }
            },
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Users_Count=="")
                    varButtons += '<a onclick="AddUserForSubProject(\'' + row.Sub_Project_Id + '\',\'' + row.Sub_Project_Name +  '\')" class="btn" style="margin-left: -16px;cursor:pointer;color: blue;" >' + row.Users_Count + '</a>';
                else
                {
                    varButtons += '<a onclick="GetUsers(\'' + row.Sub_Project_Id + '\',\''+row.Sub_Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Users_Count + '</a>';
                }
                
                return varButtons;
                }
            },
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Planned_Batches=="")
                    varButtons=row.Planned_Batches;
                else
                {
                    varButtons += '<a onclick="GetPlannedBatches(\'' + row.Sub_Project_Id + '\',\''+row.Sub_Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Planned_Batches + '</a>';
                }
                
                return varButtons;
                }
            },
            { "data": "Entity_Name"},
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Customer_Name=="")
                        varButtons=row.Customer_Name;
                    else
                    {
                        varButtons += '<a onclick="GetCustomerList(\'' + row.Customer_Id + '\')"  style="color:blue;cursor:pointer" >' + row.Customer_Name + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            
            { "data": "Project_Code"},
            { "data": "Project_Name"},
            
            { "data": "Project_Group_Name"},
            { "data": "Project_Type_Name"},
            { "data": "Block_Name"},
            { "data": "Practice_Name"},
            { "data": "Bu_Name"},
            { "data": "Product_Name"},
            { "data": "Project_Manager"},
            { "data": "Start_Date"},
            { "data": "End_Date"},
            { "data": "Status"}
            
        ],
        drawCallback: function(){
            $('#tbl_projects_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
    
}

function EditProjectDetail(ProjectId)
{
    $('#hdn_project_id').val(ProjectId);
    $('#form1').submit();
    
}

function GetCustomerList(Customer_Id){
    var URL=$('#hdn_web_url').val()+ "/GetContractbycustomer?Customer_Id="+Customer_Id;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tblTrAct tbody").empty();
            if(!jQuery.isEmptyObject(data.contracts))
            {   //alert(data.Customer_Name)
                $('#txtcustomer_name').val(data.Customer_Name);
                $('#txtfundingsource').val(data.Funding_Source);
                $('#txtcustomer_group').val(data.Customer_Group);
                $('#txtindustrytype').val(data.Industry_type);

                if (data.contracts != null){
                    var count=data.contracts.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                        {
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.contracts[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.contracts[i].Contract_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.contracts[i].Contract_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.contracts[i].Start_Date +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.contracts[i].End_Date +'</td>';
                            varHtml+='</tr>';
                        }
                        
                    }
                    $("#tblTrAct tbody").append(varHtml);
                    $('#tr_sess_act').modal('show');
                }
            }
            else
            {
                varHtml='<tr><td colspan="3" style="text-align:center;">No records found</td></tr>'
                $("#tblTrAct tbody").append(varHtml);
                $('#tr_sess_act').modal('show');
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
function GetSub_project(Project_Id){
    //alert(Project_Id)
    var URL=$('#hdn_web_url').val()+ "/Getsubprojectbyproject?Project_Id="+Project_Id;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            var varButton='';
            $("#tblsub_project tbody").empty();
            if(!jQuery.isEmptyObject(data.sub_project))
            {   //alert(data.Customer_Name)
                $('#txtproject_name').val(data.project_name);
                $('#txtprojectcode').val(data.project_code);
                $('#hdn_project_code').val(data.project_id);
                
                if (data.sub_project[0].Sub_Project_Name != null){
                    var count=data.sub_project.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                        {
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].S_No +'</td>';
                            if($('#hdn_home_user_role_id').val()=='1' || $('#hdn_home_user_role_id').val()=='15')
                                varButton='<a onclick="EditsubProjectDetail(\'' + data.sub_project[i].Sub_Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Project" class="fas fa-edit" ></i></a>';
                            varHtml+='  <td style="text-align:center;">'+ varButton +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].Sub_Project_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].Sub_Project_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].Center_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].Courses +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].Start_Date +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.sub_project[i].End_Date +'</td>';
                            varHtml+='</tr>';
                        }
                        
                    }
                    $("#tblsub_project tbody").append(varHtml);
                    $('#tr_sub_project').modal('show');
                }
                else
            {
                varHtml='<tr><td colspan="3" style="text-align:center;">No records found</td></tr>'
                $("#tblsub_project tbody").append(varHtml);
                $('#tr_sub_project').modal('show');
            }
            }
            else
            {
                varHtml='<tr><td colspan="3" style="text-align:center;">No records found</td></tr>'
                $("#tblsub_project tbody").append(varHtml);
                $('#tr_sub_project').modal('show');
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
function EditsubProjectDetail(SubProjectId)
{
    $('#hdn_subproject_id').val(SubProjectId);
    $('#form1').submit();
}
function AddUserForSubProject(SubProjectId,SubProjectName)
{
    $('#hdn_sub_project_name').val(SubProjectName);
    $('#hdn_sub_project_id').val(SubProjectId);
    $("#ddlUserRole").select2({ width: '400px' });
    $("#ddlUsers").select2({ width: '400px' });
    $("#ddlTrainerType").select2({ width: '400px' });
    $('#HdProject').text(SubProjectName);
    $('#divUsersList').modal('hide');
    $('#trainer_type').css('display', 'none');
    $('#hdn_sub_project_id').val(SubProjectId);
    $('#ddlUsers').empty();
    LoadUserRole();
   
}
function GetCourses(SubProjectId,SubProjectName)
{
    $('#HdCourse').text(SubProjectName);
    var URL=$('#hdn_web_url').val()+ "/GetCoursesBasedOnSubProject?sub_project_id="+SubProjectId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_proj_Courses").dataTable().fnDestroy();
            $("#tbl_proj_Courses tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.Courses != null){
                    count=data.Courses.length;
                    if (count>0)
                    {   varHtml='';
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.Courses[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Courses[i].Course_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Courses[i].Course_Name +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.Courses[i].Qp_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Courses[i].Qp_Name +'</td>';     
                            varHtml+='</tr>';                            
                        }
                        $("#tbl_proj_Courses tbody").append(varHtml);
                            $("#tbl_proj_Courses").DataTable();
                            $('#divCourseList').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_proj_Courses tbody").append(varHtml);
                        $('#divCourseList').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tbl_proj_Courses tbody").append(varHtml);
                $('#divCourseList').modal('show');
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

function GetUsers(SubProjectId,SubProjectName)
{
    $('#hdn_sub_project_name').val(SubProjectName);
    $('#hdn_sub_project_id').val(SubProjectId);
    $('#HdUsers').text(SubProjectName);
    var varAddButton='';
    var varRemButton='';
    var URL=$('#hdn_web_url').val()+ "/GetUsersBasedOnSubProject?sub_project_id="+SubProjectId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_proj_Users").dataTable().fnDestroy();
            $("#tbl_proj_Users tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.Users != null){
                    count=data.Users.length;
                    if (count>0)
                    {   varHtml='';
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            if($('#hdn_home_user_role_id').val()=='1' || $('#hdn_home_user_role_id').val()=='15')
                            {
                                varAddButton='<a onclick="AddUserForSubProject(\'' + data.Users[i].Sub_Project_Id + '\',\'' + SubProjectName +  '\')" class="btn" style="cursor:pointer" ><i title="Tag Users" class="fas fa-edit" ></i></a>';
                                varRemButton='<a onclick="GetUserListForSubProject(\'' + data.Users[i].Sub_Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Untag Users" class="fas fa-cut" ></i></a>';
                            }
                            varHtml+='  <td style="text-align:center;">'+ varAddButton +" "+varRemButton+'</td>';   
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Pmt +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Coo +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Cm +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Tm +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Mob +'</td>';  
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Tr +'</td>';     
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Mis +'</td>'; 
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Pco +'</td>'; 
                            varHtml+='</tr>';                            
                        }
                        $("#tbl_proj_Users tbody").append(varHtml);
                            $("#tbl_proj_Users").DataTable();
                            $('#divUsersList').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_proj_Users tbody").append(varHtml);
                        $('#divUsersList').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tbl_proj_Users tbody").append(varHtml);
                $('#divUsersList').modal('show');
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
function UntagUsers()
{
    var users='';
    $('[name=checkcase]:checked').each(function () {
        users+= $(this).val()+',';
    });
    users=users.substring(0,users.length-1)
    if (users=='')
    {
        alert('Select at least one user to untag.');
    }
    else
    {
       var URL=$('#hdn_web_url').val()+ "/untag_users_from_sub_project";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "user_ids": users,
                    "sub_project_id": $('#hdn_sub_project_id').val()
                },
                success:function(data){
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            $('#divUsersListForUntag').modal('hide');
                            GetUsers($('#hdn_sub_project_id').val(),$('#hdn_sub_project_name').val());
                           //window.location.href = '/sub_project';                          
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
function TagUsers()
{
    if ($('#ddlUsers').val()=='')
    {
        alert('Select at least one user to untag.');
    }
    else
    {
       var URL=$('#hdn_web_url').val()+ "/tag_users_from_sub_project";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "user_id": $('#ddlUsers').val(),
                    "sub_project_id": $('#hdn_sub_project_id').val()
                },
                success:function(data){
                    if(data.PopupMessage.message =="User tagged")
                    {
                        swal({   
                            title:data.PopupMessage.message,
                            text:data.PopupMessage.message+"!!",
                            icon:"success",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                $('#divUsersTag').modal('hide');
                                GetUsers($('#hdn_sub_project_id').val(),$('#hdn_sub_project_name').val())
                            //window.location.href = '/sub_project';                          
                            });

                    }
                    else{
                        swal({   
                            title:data.PopupMessage.message,
                            text:"User is already Tagged!",
                            icon:"error",
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                $('#divUsersTag').modal('hide');
                                GetUsers($('#hdn_sub_project_id').val(),$('#hdn_sub_project_name').val())
                            //window.location.href = '/sub_project';                          
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

function refresh()
{
    window.location.href = '/sub_project';  
}
function LoadUserRole(){
    var URL=$('#hdn_web_url').val()+ "/GetUserRole"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.UserRole != null)
            {
                $('#ddlUserRole').empty();
                var count=data.UserRole.length;
                if( count> 0)
                {
                    $('#divUsersTag').modal('show');
                    $('#ddlUserRole').append(new Option("ALL",0));
                    for(var i=0;i<count;i++)
                        $('#ddlUserRole').append(new Option(data.UserRole[i].User_Role_Name,data.UserRole[i].User_Role_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                { 
                    $('#divUsersTag').modal('show');
                    $('#ddlUserRole').append(new Option('No User Role','-1'));
                }
            }
        },
        error:function(err)
        {
            $('#divUsersTag').modal('hide');
            alert('Error while loading UserRole! Please try again');
            return false;
        }
    });
    return false;
}
function GetUserListForSubProject(SubProjectId)
{
    $('#hdn_sub_project_id').val(SubProjectId);
    $('#divUsersList').modal('hide');
    var URL=$('#hdn_web_url').val()+ "/GetUserListForSubProject?sub_project_id="+SubProjectId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_Users").dataTable().fnDestroy();
            $("#tbl_Users tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.Users != null){
                    count=data.Users.length;
                    if (count>0)
                    {   varHtml='';
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            varHtml += '<td style="text-align:center;"><input id="addedchk_'+data.Users[i].Userid+'" name="checkcase" type="checkbox" value="'+data.Users[i].Userid+'" ></td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Username +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Email +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Users[i].Role +'</td>';
                            varHtml+='</tr>';                            
                        }
                        $("#tbl_Users tbody").append(varHtml);
                            $("#tbl_Users").DataTable();
                            $('#divUsersListForUntag').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_Users tbody").append(varHtml);
                        $('#divUsersListForUntag').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tbl_proj_Users tbody").append(varHtml);
                $('#divUsersList').modal('show');
            }   
        },
        error:function(err)
        {
            alert('Error! Please try again jkggg');
            return false;
        }
    });
    return false;
}
function GetCenters(SubProjectId,SubProjectName)
{
    $('#headerCenter').text(SubProjectName);
    var URL=$('#hdn_web_url').val()+ "/GetCentersbasedOnSubProject?sub_project_id="+SubProjectId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_proj_centers").dataTable().fnDestroy();
            $("#tbl_proj_centers tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.Centers != null){
                    count=data.Centers.length;
                    if (count>0)
                    {   varHtml='';
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Name +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Type_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].State_Name +'</td>';     
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Region_Name +'</td>';   
                            varHtml+='</tr>';
                            
                        }
                        $("#tbl_proj_centers tbody").append(varHtml);
                            $("#tbl_proj_centers").DataTable();
                            $('#mdl_Centes').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="6" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_proj_centers tbody").append(varHtml);
                        $('#mdl_Centes').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="6" style="text-align:center;">No records found</td></tr>'
                $("#tbl_proj_centers tbody").append(varHtml);
                $('#mdl_Centes').modal('show');
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
function UploadBatchTargetMdl()
{
    
    $('#HduploadFile').text('Upload Batch Target Plan.');
    $('#imgSpinner1').hide();
    $('#mdl_upload_batch_target_plan').modal('show');
    $('#myFile').val('');
}
function DownloadBatchTargetPlanTemplate()
{
    window.location='/Bulk Upload/'+'BatchTargetPlanTemplate.xlsx';
}

function UploadFileData()
{
    
    if ($('#myFile').get(0).files.length === 0) {
        console.log("No files selected.");
    }
    else
    {
        var fileExtension = ['xlsx']
        if ($.inArray($('#myFile').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert("Formats allowed are : "+fileExtension.join(', '));
            return false;
        }
        else
        {
            UploadFileToProcess();
        }
    }
}
    /*
            $("#imgSpinner1").show();
            var files=document.getElementById("myFile").files;
            var file=files[0];

            var file_path=$('#hdn_AWS_S3_path').val()+"bulk_upload/project_planner/" + $('#hdn_home_user_id').val() + '_' + Date.now() + '_' + file.name; 
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
*/
function UploadFileToProcess()
{
    //console.log()
    var form_data = new FormData($('#formUpload')[0]);
    form_data.append('user_id',$('#hdn_home_user_id').val());
    form_data.append('user_role_id',$('#hdn_home_user_role_id').val());
    $.ajax({
        type: 'POST',
        url: $('#hdn_web_url').val()+ "/upload_batch_target_plan",
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
                            window.location.href = '/sub_project';
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
                    window.location.href = '/sub_project';
                }); 
            
        }
    });
}

function GetPlannedBatches(SubProjectId,SubProjectName)
{
    $('#HdPlannedBatches').text(SubProjectName);
    var URL=$('#hdn_web_url').val()+ "/GetSubProjectPlannedBatches?sub_project_id="+SubProjectId;
    
    $.ajax({
        type:"GET",
        url:URL,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            
            $("#tbl_planned_batches").dataTable().fnDestroy();
            $("#tbl_planned_batches tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.PlannedBatches != null){
                    count=data.PlannedBatches.length;
                    if (count>0)
                    {   varHtml='';
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            varRemButton='';
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].S_No +'</td>';
                            if($('#hdn_home_user_role_id').val()=='1' && data.PlannedBatches[i].Batch_Code =='')
                            {
                                varRemButton='<a onclick="CancelPlannedBatch(\'' + data.PlannedBatches[i].Planned_Batch_Code + '\')" class="btn" style="cursor:pointer" ><i title="Cancel Batch" class="fas fa-cut" ></i></a>';
                            }
                            varHtml+='  <td style="text-align:center;">'+varRemButton+'</td>';                               
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].Planned_Batch_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].Batch_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].Course_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].Course_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].E_Planned_Start_Date +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].E_Planned_End_Date +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].E_Target +'</td>'; 
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].C_Planned_Start_Date +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].C_Target +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].P_Planned_Start_Date +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].P_Planned_End_Date +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.PlannedBatches[i].P_Target +'</td>';     
                            varHtml+='</tr>';                            
                        }
                            $("#tbl_planned_batches tbody").append(varHtml);
                            $("#tbl_planned_batches").DataTable();
                            $('#mdl_planned_batches').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="10" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_planned_batches tbody").append(varHtml);
                        $('#mdl_planned_batches').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="10" style="text-align:center;">No records found</td></tr>'
                $("#tbl_planned_batches tbody").append(varHtml);
                $('#mdl_planned_batches').modal('show');
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

function CancelBatchSubmit(planned_batch_code)
{
    if ($('#TxtReason').val()=='')
    {
        alert('Please Enter Reason To Cancel The Batch.');
    }
    else
    {
       var URL=$('#hdn_web_url').val()+ "/cancel_planned_batch";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "user_id": $('#hdn_home_user_id').val(),
                    "planned_batch_code": planned_batch_code,
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
                                window.location.href = '/sub_project';                          
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

function CancelPlannedBatch(planned_batch_code)
{
    
    $('#hdn_planned_batch').val(planned_batch_code);
    $('#mdl_planned_batches').modal('hide');
    $('#mdl_cancel_batch').modal('show');
    
}

function DownloadTableBasedOnFilter(){
    $("#imgSpinner").show();
    // from candidate
    if($('#To_Date').val()=='')
        {
            alert("Please select date.");
            $("#imgSpinner").hide();
        }
    else{
        var URL=$('#hdn_web_url').val()+ "/download_sub_project_list"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                        "entity":$('#ddlEntity').val().toString(),
                        "customer":$('#ddlCustomer').val().toString(),
                        "p_group":$('#ddlP_Group').val().toString(),
                        "block":$('#ddlBlock').val().toString(),
                        "practice":$('#ddlPractice').val().toString(),
                        "bu":$('#ddlBU').val().toString(),
                        "product":$('#ddlProduct').val().toString(),
                        "status":$('#ddlStatus').val().toString(),
                        "project":$('#ddlProject').val().toString(),

                        "user_id":$('#hdn_home_user_id').val(),
                        "user_role_id":$('#hdn_home_user_role_id').val(),
                        "user_region_id":$('#hdn_user_region_id').val()
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
                            console.log(resp)
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