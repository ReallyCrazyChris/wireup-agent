# tries to coerce a value according to a proptype
# value any values
# proptype string to coerce the value to
def coerce(value,proptype):

  if proptype == "string":
    return str(value)
  
  if proptype == "integer":
    
    if (value==True or value=="true"):
      return 1

    try: 
      return int(float(value))  # TODO may not work in small processor ?
    
    except ValueError:
      return 0

  if proptype == "boolean":
    if (value == False or value == 0 or value == "" or value == "false"):
      return False
    else:
      return True

  if proptype == "url":
    return str(value) 