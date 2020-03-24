var varTable;
var IsActive;
$(document).ready(function () {
    //IsActive='{{active}}';
    // if ('{{active}}'!="")
    //     IsActive=0;
    console.log(IsActive);
    $("#tbl_clients").dataTable().fnDestroy();
    $('.dropdown-search-filter').select2({
        placeholder:''
    });
    LoadFunding_Resourcesdl();
    LoadCustomer_Groupdl();
    LoadSalesCategoryddl();
    role_id=parseInt($('#hdn_home_user_role_id').val());
                if(role_id == 1)
                    $('#btn_create').show();
                else 
                    $('#btn_create').hide();

    LoadTable(); 


});


function LoadFunding_Resourcesdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Funding_resources"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Funding_Resources != null)
            {
                $('#ddlFundingSource').empty();
                var count=data.Funding_Resources.length;
                if( count> 0)
                {
                    //$('#ddlFundingSource').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlFundingSource').append(new Option(data.Funding_Resources[i].Funding_Source_Name,data.Funding_Resources[i].Funding_Source_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlFundingSource').append(new Option('ALL','-1'));
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

function LoadCustomer_Groupdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Customer_Group"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "customer_group_id" : 0 //$('#ddlRM_role').val().toString()//$('#ddlProject option:selected').val()
        },
        success: function (data){
            if(data.Customer_Group != null)
            {
                $('#ddlcustomergroup').empty();
                var count=data.Customer_Group.length;
                if( count> 0)
                {
                    //$('#ddlcustomergroup').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlcustomergroup').append(new Option(data.Customer_Group[i].Customer_Group_Name,data.Customer_Group[i].Customer_Group_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlcustomergroup').append(new Option('ALL','-1'));
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

function LoadSalesCategoryddl(){
    var URL=$('#hdn_web_url').val()+ "/GetAllCategoryTypes"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.CategoryType != null)
            {
                $('#ddlCategoryType').empty();
                var count=data.CategoryType.length;
                if( count> 0)
                {
                    for(var i=0;i<count;i++)
                        $('#ddlCategoryType').append(new Option(data.CategoryType[i].Category_Type_Name,data.CategoryType[i].Category_Type_Id));
                    
                }
                else
                {
                    $('#ddlCategoryType').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Category Type! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTable()
{
    vartable1 = $("#tbl_clients").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/client_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.client_id = 0;
                d.funding_sources=$('#ddlFundingSource').val().toString();
                d.is_active=-1;
                d.customer_groups = $('#ddlcustomergroup').val().toString();
                d.category_type_ids = $('#ddlCategoryType').val().toString();
            },
            error: function (e) {
                $("#tbl_clients tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},  
            {"visible": false,
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditClientDetail(\'' + row.Client_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Client_Name" },
            { "data": "Client_Code" },
            { "data": "Funding_Source_Name" },
            { "data": "Customer_Group_Name" },
            { "data": "Category_Type_Name" },
            { "data": "Industry_Type_Name" }
          
        ],
        // "ColumnDefs"  :[
        //     {
        //         "visible": false,
        //         "targets": [ 1 ],                
        //         "searchable": false,
        //         "ordering":false
        //     }
        // ],
        drawCallback: function(){
            $('#tbl_clients_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditClientDetail(ClientId)
{
    $('#hdn_client_id').val(ClientId);
    $('#form1').submit();
    
}