



function addProcessor(_data, _success, _error)
{
  var loader = $.ajax(...);
  loaderMap[loader] = {data:_data, success:_success, error:_error};
}
function postHandler(data, status, loader)
{
  var processor = loaderMap[loader];
  ...
}
