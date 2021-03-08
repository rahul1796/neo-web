var varTable;
const months = ["Jan", "Feb", "Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]; 
     
$(document).ready(function () {
    $("#imgSpinner").hide();
    $('.dropdown-search-filter').select2();
    $(".date-picker").flatpickr({
        dateFormat:'M-Y',
        minDate: 'Apr.2019'
    }); 
   
    $("#tbl_user_sub_project").dataTable().fnDestroy();
    //Loadcandidatestatusddl();
    LoadStageStausddl();
    LoadCustomers();
    LoadRegionddl();
    role_id=parseInt($('#hdn_home_user_role_id').val());
    //LoadTable();
});
function LoadStageStausddl()
    {
        // $('#ddlStage').empty();
        // $('#ddlStage').append(new Option('Yet To Start','0'));
        // $('#ddlStage').append(new Option('Open','1'));
        // $('#ddlStage').append(new Option('Expired','2'));
        $('#ddlStatus').empty();
        $('#ddlStatus').append(new Option('All','-1'));
        $('#ddlStatus').append(new Option('Active','1'));
        $('#ddlStatus').append(new Option('Inactive','0'));    
    }
    function LoadCustomers(){
        var URL=$('#hdn_web_url').val()+ "/GetALLClientBasedOnStatus"
        $.ajax({
            type:"GET",
            url:URL,
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            data:{
                "user_id": $('#hdn_home_user_id').val(),
                "user_role_id": $('#hdn_home_user_role_id').val(),
                "status_id": $('#ddlStatus').val()

            },
            success: function (data){
                if(data.Clients != null)
                {
                    $('#ddlCustomer').empty();
                    var count=data.Clients.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                            $('#ddlCustomer').append(new Option(data.Clients[i].Customer_Name,data.Clients[i].Customer_Id));
                    }
                    else
                    {
                     //   $('#ddlCustomer').append(new Option('Choose Customer',''));
                    }
                }
            },
            error:function(err)
            {
                alert('Error loading customers! Please try again');
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
function loadbasedonclient()
{
    //alert($('#ddlClient').val().toString());
    //LoadContract();
    LoadProject();
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

function DownloadTableBasedOnSearch(){
    $("#imgSpinner").show(); 
    if (0==9){
    console.log(false)
    }
    else{ 
        $("#imgSpinner").show();       
        var URL=$('#hdn_web_url').val()+ "/user_sub_project_list_download"
        var to_date = new Date($('#MonthYear').val());
        
        //window.location = URL + "?ActivityDate=2019-09-09"
        $.ajax({
            type: "POST",
            dataType: "json",
            url: URL,
            data:{
                user_id : $('#hdn_home_user_id').val(),
                user_role_id  : $('#hdn_home_user_role_id').val(),
                customer : $('#ddlCustomer').val().toString(),
                project : $('#ddlProject').val().toString(),
                sub_project : $('#ddlSubProject').val().toString(),
                region : $('#ddlRegion').val().toString(),
                user_status : $('#ddlUserStatus').val().toString(),
                sub_project_status : $('#ddlSubProjectStatus').val().toString(),
                month: to_date.getMonth(),
                year: to_date.getFullYear(),
                status_id : $('#ddlStatus').val()
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

function LoadTable()
{
    var course_selected="",data='';
    var count;
    vartable = $("#tbl_user_sub_project").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/user_sub_project_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id = $('#hdn_home_user_id').val();
                d.user_role_id  = $('#hdn_home_user_role_id').val();
                d.customer = $('#ddlCustomer').val().toString();
                d.project = $('#ddlProject').val().toString();
                d.sub_project = $('#ddlSubProject').val().toString();
                d.region = $('#ddlRegion').val().toString();
                d.user_status = $('#ddlUserStatus').val().toString();
                d.sub_project_status = $('#ddlSubProjectStatus').val().toString();
                d.status_id = $('#ddlStatus').val();
                 },
            error: function (e) {
                $("#tbl_user_sub_project tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Employee_Code" },
            { "data": "Employee_Name" },
            { "data": "Employee_Email" },
            { "data": "Sub_Project_Code"},
            { "data": "Sub_Project_Name" },
            { "data": "Employee_Neo_Role" },
            { "data": "Employement_Type" }         
            
        ],
        drawCallback: function(){
            $('#tbl_user_sub_project_paginate ul.pagination').addClass("pagination-rounded");
        }


    });
}


/*function DownloadTableBasedOnSearch()
{
    var URL=$('#hdn_web_url').val()+ "/user_sub_project_download";
    $.ajax({
        type:"POST",
        url:URL,
        data:{
            user_id = $('#hdn_home_user_id').val(),
            user_role_id  = $('#hdn_home_user_role_id').val(),
            customer = $('#ddlClient').val().toString(),
            project = $('#ddlProject').val().toString(),
            sub_project = $('#ddlSubProject').val().toString(),
            region = $('#ddlRegion').val().toString(),
            user_status = $('#ddlUserStatus').val().toString(),
            sub_project_status = $('#ddlSubProjectStatus').val().toString()
        },
        success:function(data){
            alert(data);     
           
                
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
}
*/