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

function LoadTable()
{
    vartable1 = $("#tbl_projects").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/project_list",
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
            // function (){
            //     if($('#hdn_home_user_role_id').val()=='1')
            //         return true;
            //     else return false;
            // },
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditProjectDetail(\'' + row.Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Project" class="fas fa-edit" ></i></a>';
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
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Project_Code=="")
                        varButtons=row.Project_Code;
                    else
                    {
                        varButtons += '<a onclick="GetSub_project(\'' + row.Project_Id + '\')"  style="color:blue;cursor:pointer" >' + row.Project_Code + '</a>';
                    }
                    
                    return varButtons;
                    }
            },
            { "data": "Project_Name"},
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Center_Count=="")
                    varButtons=row.Center_Count;
                else
                {
                    varButtons += '<a onclick="GetCenters(\'' + row.Project_Id + '\',\''+row.Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Center_Count + '</a>';
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
                    varButtons += '<a onclick="GetCourses(\'' + row.Project_Id + '\',\''+row.Project_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Course_Count + '</a>';
                }
                
                return varButtons;
                }
            },
            { "data": "Project_Group_Name"},
            { "data": "Project_Type_Name"},
            { "data": "Block_Name"},
            { "data": "Practice_Name"},
            { "data": "Bu_Name"},
            { "data": "Product_Name"},
            { "data": "Project_Manager"},
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
                            console.log(data.sub_project[i].Sub_Project_Id)
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
    $('#form2').submit();
}
function GetCourses(ProjectId,ProjectName)
{
    $('#HdCourse').text(ProjectName);
    var URL=$('#hdn_web_url').val()+ "/GetCoursesForProject?project_id="+ProjectId;
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
                        console.log(count);
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

function GetCenters(ProjectId,ProjectName)
{
    $('#headerCenter').text(ProjectName);
    var URL=$('#hdn_web_url').val()+ "/GetCentersForProject?project_id="+ProjectId;
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
                        console.log(count);
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