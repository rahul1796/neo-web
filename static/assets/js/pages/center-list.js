var varTable;

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
    
function LoadBuddl(){
    var URL=$('#hdn_web_url').val()+ "/GetAllBusBasedOn_User"
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
            if(data.Bu != null)
            {
                $('#ddlBu').empty();
                var count=data.Bu.length;
                if( count> 0)
                {
                    //$('#ddlCenter').append(new Option('ALL',''));
                    for(var i=0;i<count;i++)
                        $('#ddlBu').append(new Option(data.Bu[i].Bu_Name,data.Bu[i].Bu_Id));
                    $('#ddlBu').val('');
                }
                else
                {
                    $('#ddlBu').append(new Option('ALL',''));
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


function LoadCourseddl(){
    var URL=$('#hdn_web_url').val()+ "/Get_All_Courses"
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
                    $('#ddlCourse').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCourse').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlCourse').append(new Option('ALL','-1'));
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


//LoadClusterddl
function LoadClusterddl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Cluster_Based_On_Region"
        $.ajax({
        type:"POST",
        url:URL,
        async:false,       
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json", 
        data:{
            "region_id" : $('#ddlRegion').val().toString()//$('#ddlProject option:selected').val()
        },
		success: function (data){
            if(data.States != null)
            {
                $('#ddlCluster').empty();
                var count=data.States.length;
                if( count> 0)
                {
                    //$('#ddlCluster').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCluster').append(new Option(data.States[i].State_Name,data.States[i].State_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlCluster').append(new Option('ALL','-1'));
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

function LoadTable()
{
    vartable1 = $("#tbl_centers").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/center_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.center_id = 0,
                d.user_id= $('#hdn_home_user_id').val(),
                d.user_role_id = $('#hdn_home_user_role_id').val(),
                d.user_region_id = $('#hdn_user_region_id').val(),
                d.center_type_ids=$('#ddlCenterType').val().toString(),
                d.bu_ids=$('#ddlBu').val().toString(),
                d.status=$('#ddlStatus').val().toString(),
				d.regions=$('#ddlRegion').val().toString(),
				d.clusters=$('#ddlCluster').val().toString(),
				d.courses=$('#ddlCourse').val().toString()
            },
            error: function (e) {
                $("#tbl_centers tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"orderable": false,
                "data": function (row, type, val, meta) {
                var varButtons = ""; 
                //varButtons += '<a onclick="EditCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Center" class="fas fa-edit" ></i></a><a onclick="AddSubCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Add SubCenter" class="fas fa-plus" ></i></a>';
                varButtons+='<a onclick="GetProjectDetails(\'' + row.Center_Id + '\',\'' + row.Center_Name + '\')" class="btn" style="cursor:pointer" ><i title="Associated Projects" class="fas fa-list-ul" ></i></a>'
                return varButtons;
                }
            },
            { "data": "Center_Code" },
            { "data": "Center_Name" },
            { "data": "Center_Type_Name"},
            { "data": "Location" },
            { "data": "District_Name"},
            { "data": "State_Name" },                       
            { "data": "Region_Name"},
            { "visible": false,"data": "Country_Name"},
            {"data":"Is_Active"},
            //{"data":"Course_Count"},
            { 
              "data": 
              function (row, type, val, meta) {
                  var varButtons = ""; 
                  if(row.Course_Count==0)
                      varButtons=row.Course_Count;
                  else
                  {
                      varButtons += '<a onclick="GetCourseDetails(\'' + row.Center_Id + '\',\'' + row.Center_Name + '\')"  style="color:blue;cursor:pointer" >' + row.Course_Count + '</a>';
                  }                    
                  return varButtons;
              }
           }
        ],
        "ColumnDefs":[
            {
                orderable:false,
                targets:[1]
            }
        ],
        drawCallback: function(){
            $('#tbl_centers_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditCenterDetail(CenterId)
{
    $('#hdn_center_id').val(CenterId);
    $('#form1').submit();
    
}
function AddSubCenterDetail(ParentCenterId)
{
    //alert(ParentCenterId);
    $('#hdn_center_id').val(ParentCenterId);
    $('#form1').attr('action', '/assign_parent_center_id_for_sub_center');
    //alert($('#hdn_parent_center_id').val());
    $('#form1').submit();
}

function LoadTableBasedOnSearch()
{
    // alert($('#ddlCenterType').val().toString());
    // alert($('#ddlBu').val().toString());
    // alert($('#ddlStatus').val().toString());
    LoadTable();
}

function Download()
    {                   
        var URL=$('#hdn_web_url').val()+ "/download_centers_list";            
        $.ajax({
            type:"POST",
            url:URL,
            async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            data:{         
                "center_type_ids":$('#ddlCenterType').val().toString(),
                "bu_ids":$('#ddlBu').val().toString(),
                "status":$('#ddlStatus').val().toString()
            },
            success:function(data){
                if(data!=null)
                {
                    window.location=data.FilePath+data.FileName+'.xlsx';
                }                    
            },
            error:function(x){
                alert('Error while downloading Report. ');
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
                            varHtml+='  <td style="text-align:center;">'+ CenterName +'</td>';
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

function GetCourseDetails(CenterId,CenterName)
{
    $('#HdCourse').text(CenterName);
    var URL=$('#hdn_web_url').val()+ "/GetCoursesForCenter?center_id="+CenterId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tblCourses").dataTable().fnDestroy();
            $("#tblCourses tbody").empty();
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
                        $("#tblCourses tbody").append(varHtml);
                            $("#tblCourses").DataTable();
                            $('#divCourseList').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                        $("#tblCourses tbody").append(varHtml);
                        $('#divCourseList').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tblCourses tbody").append(varHtml);
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