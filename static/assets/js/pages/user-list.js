
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
            {"visible": false,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id != 5)
                    varButtons += '<a onclick="EditUserDetail(\'' + row.User_Id + '\',\'' + row.User_Role_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a>';
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
            { "data": "Entity_Name" },
            { "data": "Department_Name" },
            { "data": "Employee_Role_Name" },
            { "data": "User_Role_Name" },
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

function EditUserDetail(UserId,UserRoleId)
{
    $('#hdn_user_id').val(UserId);
    //alert('Hi');
    $('#form1').submit();
    
}
function GetProjectDetails(User_Id,User_Name)
{
    var URL=$('#hdn_web_url').val()+ "/GetSubProjectsForUser?user_id="+User_Id;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
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
                                varHtml+='  <td style="text-align:center;">'+'<a onclick="EditModal(\'' + data.UserTarget[i].From_Date_Form + '\',\'' + data.UserTarget[i].To_Date_Form + '\',\'' + data.UserTarget[i].Target + '\',\'' + data.UserTarget[i].User_Id + '\',\'' + data.UserTarget[i].Is_Active + '\',\'' + data.UserTarget[i].User_Target_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Room" class="fas fa-edit" ></i></a>'+'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].From_Date +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].To_Date +'</td>';                    
                                varHtml+='  <td style="text-align:center;">'+ data.UserTarget[i].Target +'</td>';
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
        $('#target').val('');
        $('#hdn_user_target_id').val("0");
        $('#hdn_user_id_m2').val($('#hdn_modal_user_id').val()); 
        
        //$('#mdl_room_center').modal('hide');
        $('#mdl_add_edit_targets').modal('show');
    }
    
    function EditModal(From_Date, To_Date, Target, User_Id, Is_Active, User_Target_Id)
    {   
        if(Is_Active)
            $('#isactive').prop('checked',true);
        else 
            $('#isactive').prop('checked',false);
        $('#From_Date').val(From_Date);
        $('#To_Date').val(To_Date);
        $('#target').val(Target);
        $('#hdn_user_target_id').val(User_Target_Id);
        $('#hdn_user_id_m2').val($('#hdn_modal_user_id').val()); 
        //$('#mdl_room_center').modal('hide');
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

        //alert($('#target').val())

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
                "user_target_id":$('#hdn_user_target_id').val()
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
    
    function onchange_roomtype(){
        if ($('#Room_Type').val() == 'Others'){
            $('#ddl_If_Others').show()
        }
        else{
            $('#ddl_If_Others').hide()
        }
    }
