


function addProcessor(_data, _success, _error)
{
  var loader = $.ajax(...).done(function(data){
    var processor = loaderMap[loader];
    ...
    loaderMap[loader] = undefined;
  }).fail(function(){
    loaderMap[loader] = undefined;
  });
  loaderMap[loader] = {data:_data, success:_success, error:_error};
}
