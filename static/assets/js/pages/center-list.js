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

function LoadmapCourseddl(){
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
                $('#map_course').empty();
                var count=data.Courses.length;
                if( count> 0)
                {
                    //$('#map_course').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#map_course').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#map_course').append(new Option('ALL','-1'));
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
        "table-layout": "fixed",
        "scrollX": true,
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
            {"visible": ($('#hdn_home_user_role_id').val()=='1'||$('#hdn_home_user_role_id').val()=='15')?true:false,
            
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Center" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Center_Code" },
            { "data": "Center_Name" },
            { "data": "Center_Type_Name"},
            { "data": "Partner_Name"},
            { 
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Sub_Project_Count==0)
                        varButtons=row.Sub_Project_Count;
                    else
                    {
                        varButtons += '<a onclick="GetProjectDetails(\'' + row.Center_Id + '\',\'' + row.Center_Name + '\')"  style="color:blue;cursor:pointer" >' + row.Sub_Project_Count + '</a>';
                    }                    
                    return varButtons;
                }
            },
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
            },
            { 
                "data": function (row, type, val, meta) {
                    var varButtons = ""; /*
                    if(row.User_Count=="")
                        varButtons=row.User_Count;
                    else
                    {
                        varButtons += '<a onclick="GetPartnerUsers(\'' + row.Partner_Id + '\',\''+row.Partner_Type_Id+ '\')"  style="color:blue;cursor:pointer" >' + row.User_Count + '</a>';
                    }*/
                    varButtons += '<a onclick="GetRoomCenters(\'' + row.Center_Id + '\',\'' + row.Center_Name +'\')"  style="color:blue;cursor:pointer" >' + row.Room_Count + '</a>';
                    return varButtons;
                    }
            },
            { 
                "data": 
                function (row, type, val, meta) {
                    var varButtons = "";
                    if(row.Geo_Location=="" || row.Geo_Location=="null")
                        varButtons=row.Geo_Location;
                    else
                    {
                        varButtons += '<a href="' + row.Geo_Location +  '" target="_blank" title="View location map"><img src="static/images/location.png" style="height:20px;"/></a>';
                    }                    
                    return varButtons;
                }
            },
            { "data": "Location"},
            { "data": "District_Name"},
            { "data": "State_Name" },                       
            { "data": "Region_Name"},
            { "visible": false,"data": "Country_Name"},
            {"data":"Is_Active"}
            //{"data":"Course_Count"}
            
        ],
        "ColumnDefs":[
            {
                orderable:false,
                targets:1
            },
            {
                orderable:false,
                targets:7
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

function DownloadTableBasedOnSearch()
{                   
    $("#imgSpinner").show();
    // from candidate
    if(0==1)
        {
            
            $("#imgSpinner").hide();
        }
    else{
        var URL=$('#hdn_web_url').val()+ "/download_centers_list"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                        "center_id":0,
                        "user_id":$('#hdn_home_user_id').val(),
                        "user_role_id":$('#hdn_home_user_role_id').val(),
                        "user_region_id":$('#hdn_user_region_id').val(),
                        "center_type_ids":$('#ddlCenterType').val().toString(),
                        "bu_ids":$('#ddlBu').val().toString(),
                        "status":$('#ddlStatus').val().toString(),
                        "regions":$('#ddlRegion').val().toString(),
                        "clusters":$('#ddlCluster').val().toString(),
                        "courses":$('#ddlCourse').val().toString()                        
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

function GetRoomCenters(CenterId,CenterName)
    {
        $('#hdn_modal_center_id').val(CenterId);
        $('#headerRooms').text(CenterName);
        var URL=$('#hdn_web_url').val()+ "/GetCenterRooms?center_id="+CenterId;
        $.ajax({
            type:"GET",
            url:URL,
            async:false,
            overflow:true,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                varHtml='';
                $("#tbl_rooms").dataTable().fnDestroy();
                $("#tbl_rooms tbody").empty();
                if(!jQuery.isEmptyObject(data))
                {   if (data.CenterRooms != null){
                        count=data.CenterRooms.length;
                        if (count>0)
                        {   varHtml='';
                            //console.log(data.CenterRooms[0].Course_Ids);
                            for(var i=0;i<count;i++)
                            {
                                td_open= '  <td style="text-align:center;">' ;
                                td_close=   '</td>';       
                                varHtml+='<tr>';
                                varHtml+='  <td style="text-align:center;">'+ data.CenterRooms[i].S_No +'</td>';
                                varHtml+='  <td style="text-align:center;">'+'<a onclick="beforeEditModal(\'' + data.CenterRooms[i].Room_Name + '\',\'' + data.CenterRooms[i].Room_Type + '\',\'' + data.CenterRooms[i].Room_Size + '\',\'' + data.CenterRooms[i].Room_Capacity + '\',\'' + data.CenterRooms[i].Is_Active + '\',\'' + data.CenterRooms[i].Room_Id + '\',\'' + data.CenterRooms[i].Center_Id + '\',\'' + data.CenterRooms[i].Center_Name + '\',\'' + data.CenterRooms[i].Course_Ids  + '\')" class="btn" style="cursor:pointer" ><i title="Edit Room" class="fas fa-edit" ></i></a>'+'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.CenterRooms[i].Room_Name +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.CenterRooms[i].Room_Type +'</td>';                    
                                varHtml+='  <td style="text-align:center;">'+ data.CenterRooms[i].Room_Size +'</td>';
                                varHtml+='  <td style="text-align:center;">'+ data.CenterRooms[i].Room_Capacity +'</td>';  
                                varHtml+='  <td style="text-align:center; white-space:normal;">'+ data.CenterRooms[i].Course_Name +'</td>';  
                                varHtml+='</tr>';                            
                            }
                            $("#tbl_rooms tbody").append(varHtml);
                                $("#tbl_rooms").DataTable({
                                drawCallback: function(){
                                    $('#tbl_users_paginate ul.pagination').addClass("pagination-rounded");
                                }
                            });
                                $('#mdl_room_center').modal('show');
                                varHtml='';
                        }
                        else
                        {
                            //varHtml='<tr><td colspan="4" style="text-align:center;">No records found</td></tr>'                            
                            //$("#tbl_users tbody").append(varHtml);
                            $("#tbl_rooms").DataTable();
                            $('#mdl_room_center').modal('show');
                        } 
                        
                    }
                }
                else
                {
                    //varHtml='<tr><td colspan="4" style="text-align:center;">No records found</td></tr>'
                    //$("#tbl_users tbody").append(varHtml);
                    $("#tbl_rooms").DataTable();
                    $('#mdl_room_center').modal('show');
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
        $('#Room_Type').empty();
        $('#Room_Type').append(new Option('Class room','Class room'));
        $('#Room_Type').append(new Option('Lab','Lab'));
        $('#Room_Type').append(new Option('Reception','Reception'));
        $('#Room_Type').append(new Option('Others','Others'));

        LoadmapCourseddl();
        $('#ddl_If_Others').hide();
        $('#isactive').prop('checked',true);
        $('#Room_Name').val('');
        $('#Room_Size').val('');
        $('#Room_Capacity').val('');
        $('#hdn_room_id').val("0");
        $('#hdn_center_id_m2').val($('#hdn_modal_center_id').val()); 
        
        //$('#mdl_room_center').modal('hide');
        $('#mdl_add_edit_rooms').modal('show');
    }
    function beforeEditModal(Room_Name, Room_Type, Room_Size, Room_Capacity, Is_Active, Room_Id, Center_id, Center_Name,Course_Ids){
        LoadmapCourseddl();
        
        $('#Room_Type').empty();
        $('#Room_Type').append(new Option('Class room','Class room'));
        $('#Room_Type').append(new Option('Lab','Lab'));
        $('#Room_Type').append(new Option('Reception','Reception'));
        $('#Room_Type').append(new Option('Others','Others'));

        EditModal(Room_Name, Room_Type, Room_Size, Room_Capacity, Is_Active, Room_Id, Center_id, Center_Name,Course_Ids);
    }
    function EditModal(Room_Name, Room_Type, Room_Size, Room_Capacity, Is_Active, Room_Id, Center_id, Center_Name,Course_Ids)
    {   
        if(Is_Active)
            $('#isactive').prop('checked',true);
        else 
            $('#isactive').prop('checked',false);
        //alert(Room_Type)
        var rt=''
        if ((Room_Type=='Class room')|(Room_Type=='Lab')|(Room_Type=='Reception')){
            $('#Room_Type').val(Room_Type);
            $('#ddl_If_Others').hide();
        }
        else{
            $('#ddl_If_Others').show();
            $('#Room_Type').val('Others');
            $('#If_Others').val(Room_Type);
        }
        
        
        $('#Room_Name').val(Room_Name);
        $('#Room_Size').val(Room_Size);
        $('#Room_Capacity').val(Room_Capacity);
        $('#hdn_room_id').val(Room_Id);
        $('#hdn_center_id_m2').val(Center_id);
        var ar = Course_Ids.split(",")
        $('#map_course').val(ar).trigger('change');

        //$('#mdl_room_center').modal('hide');
        $('#mdl_add_edit_rooms').modal('show');
        
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
                console.log(response);
                //UploadFileToProcess();
            }
            else{
                alert("Could not upload file to s3.");
            }
        }
        };
        xhr.send(postData);
    }

    function UploadFileData(file,file_name)
    {
        // var files=document.getElementById("myFile").files;
        // var file=files[0];

        var file_path=$('#hdn_AWS_S3_path').val()+"bulk_upload/room_image/" + file_name; 
        var api_url=$('#hdn_COL_url').val() + "s3_signature?file_name="+file_path+"&file_type="+file.type;
        
        var xhr = new XMLHttpRequest();
        xhr.open("GET",api_url );
            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4){
                if(xhr.status === 200){
                    var response = JSON.parse(xhr.responseText);
                    console.log(response);
                    uploadFileToS3(file, response.data, response.url);
                }
                else{
                    alert("Could not get signed URL.");
                }
                }
            };
            xhr.send();
        
    }

    function AddeEditCenterRoom()
    {
        var room_type=''
        if ($('#Room_Type').val() == 'Others'){
            room_type = $('#If_Others').val()
        }
        else{
            room_type = $('#Room_Type').val()
        }
        var ins = document.getElementById('images').files.length;
        //alert(ins);
        var validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
        var imstatus=1;
        var sizestatus=1;
        for (var x = 0; x < ins; x++) {
            var file = document.getElementById('images').files[x]
            //console.log(file.size)
            if (file.size > 1024*1024) { 
                sizestatus=0;
            }
            //alert()
            if (!validImageTypes.includes(file['type'])) {
                imstatus=0;
            }
        }
        if (imstatus==0){
            alert('Image format is not valid')
        }
        else if (sizestatus==0){
            alert('Image size is not valid')
        }
        else{

            var filename=[]
            var file_name = ''
            for (var x = 0; x < ins; x++) {
                var file = document.getElementById('images').files[x]
                file_name=$('#hdn_center_id_m2').val() + '_' +room_type+'_' + file.name
                UploadFileData(file,file_name)
                filename.push(file_name)
        }
        //console.log()
        var form_data = new FormData(); //$('#formUpload')[0]
        form_data.append('Room_Name',$('#Room_Name').val());
        form_data.append('Room_Type',room_type);
        form_data.append('Room_Size',$('#Room_Size').val());
        form_data.append('Room_Capacity',$('#Room_Capacity').val());
        form_data.append('isactive',$('#isactive').prop('checked'));
        form_data.append('center_id',$('#hdn_center_id_m2').val());
        form_data.append('room_id',$('#hdn_room_id').val());
        form_data.append('course_ids',$('#map_course').val().toString());
        form_data.append('room_images',filename.toString());

        console.log(filename.toString())
        // for (var x = 0; x < ins; x++) {
        //     form_data.append("fileToUpload[]", document.getElementById('images').files[x]);

        var URL=$('#hdn_web_url').val()+ "/add_edit_center_room";
        $.ajax({
            type:"POST",
            url:URL,
            enctype: 'multipart/form-data',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            
            // data:{
            //     "Room_Name" : $('#Room_Name').val(),
            //     "Room_Type" : room_type,
            //     "Room_Size" : $('#Room_Size').val(),
            //     "Room_Capacity" : $('#Room_Capacity').val(),
            //     "isactive" : $('#isactive').prop('checked'),
            //     "center_id":$('#hdn_center_id_m2').val(),
            //     "room_id":$('#hdn_room_id').val(),
            // },
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
                                window.location.href = '/center';
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
    function onchange_roomtype(){
        if ($('#Room_Type').val() == 'Others'){
            $('#ddl_If_Others').show()
        }
        else{
            $('#ddl_If_Others').hide()
        }
    }