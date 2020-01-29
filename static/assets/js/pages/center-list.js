var varTable;
$(document).ready(function () {
    $("#tbl_centers").dataTable().fnDestroy();
    
    $('.dropdown-search-filter').select2({
        placeholder:'select an option'
    });
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
    LoadCenterType();
    LoadBuddl();
    LoadTable(); 
});

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
                d.center_type_ids=$('#ddlCenterType').val().toString(),
                d.bu_ids=$('#ddlBu').val().toString(),
                d.status=$('#ddlStatus').val().toString()
            },
            error: function (e) {
                $("#tbl_centers tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": false,
                "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id != 5)
                    varButtons += '<a onclick="EditCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Center" class="fas fa-edit" ></i></a><a onclick="AddSubCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Add SubCenter" class="fas fa-plus" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Center_Name" },
            { "data": "Center_Type_Name"},
            //{ "data": "Center_Category_Name" },
            { "data": "Bu_Name"},
            { "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            },
            { "data": "Region_Name"},
            { "data": "Cluster_Name"},
            { "data": "Country_Name"},
            { "data": "State_Name" },
            { "data": "District_Name"},
            { "data": "Location" }
            
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
