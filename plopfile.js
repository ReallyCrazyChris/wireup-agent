
const inquirerRecursive = require('inquirer-recursive');
const shell = require('shelljs');
const SerialPort = require('serialport');

const confirmRerquiredSoftware = function(){
  if (!shell.which('esptool.py.exe')) {
    shell.echo('Sorry, this script requires esptool.py.exe');
    shell.exit(1);
  }

  if (!shell.which('ampy.exe')) {
    shell.echo('Sorry, this script requires ampy.exe');
    shell.exit(1);
  }
}

const comport_prompt =  {
  type: 'list',
  name: 'comport',
  message: 'specify the comport e.g dev/ttyUSB0 or COM1',
  choices:function(){
    const result = []
    return new Promise((resolve, reject) => {
      SerialPort.list(function (err, ports) {
        ports.forEach(function(port) {
          result.push(port.comName)
        });
        resolve(result);
      });
    });

  }
}

const selectproductfolder_prompt = {
  type: 'list',
  name: 'foldername',
  message: 'select the product folder',

  choices:function(){
    const foldernames = []
    shell.ls('-d','./src/products/*').forEach(function (file) {
      foldernames.push(file.split('/').pop())
    })
    return foldernames
  }
}

const selectcorefile_prompt = {
    type: 'list',
    name: 'filename',
    message: 'select the core file',

    choices:function(){
      const filenames = []
      shell.ls('./internals/core/*').forEach(function (file) {
        filenames.push(file.split('/').pop())
      })
      return filenames
    }
}

const  selectfirmware_prompt = {
  type: 'list',
  name: 'flashfile',
  message: 'Select the firmware for your product',
  choices:function(){

    const filenames = []
    shell.ls('./internals/bin/*').forEach(function (file) {
      filenames.push(file)
    })
    return filenames

  }
}




module.exports = function (plop) {
    // WireUP product 
    
    confirmRerquiredSoftware()

    plop.setPrompt('recursive', inquirerRecursive);
    plop.setHelper('typename',(txt) => txt.toLowerCase().replace(/\s/g,''));
    plop.setHelper('lowercase',(txt) => txt.toLowerCase().replace(/\s/g,''));
    plop.setHelper('indexadjust',(index) => Number(index) + 4);
    plop.setHelper('pseudorandomkey',() => Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 15) );

    plop.setHelper('stringAssist', function (value) {
        switch(typeof value){
              case 'number': return value;
              case 'boolean': return value ? "True" : "False"
              case 'string': return "'"+value+"'";
        }
    });

    plop.setGenerator('create', {
        description: ' the scafholding for a working product',
        prompts: [
        {
            type: 'input',
            name: 'company',
            message: 'product manufacturer name',
            default: 'WireUP'
        },
        {
            type: 'input',
            name: 'name',
            message: 'product name',
            default: 'WireUP Thing'
        },
        {
            type: 'input',
            name: 'description',
            message: 'product description',
            default: 'an IoT device enabled by WireUP'
        },

        {   type: 'recursive',
            message: 'Add a property ?',
            name: 'meta',
            prompts: [
                  {
                			type: 'input',
                			name: 'name',
                			message: 'propertie\'s name?',
                      default: 'Button',
                			validate: function (value) {
                      	if ((/.+/).test(value)) { return true; }
                				return 'property name is required';
                			},
                	},
                  {
                      type: 'input',
                      name: 'label',
                      message: 'propertie\'s label?',
                      default: function(answers){ return answers.name},
                      validate: function (value) {
                        if ((/.+/).test(value)) { return true; }
                        return 'property name is required';
                      },
                  },
                  {
                    type: 'list',
                    name: 'type',
                    message: 'Select the literal type of the property?',
                    choices:['boolean','integer','string','url','time'],
                    default:'boolean',
                  },
                  {
                      type: 'list',
                      name: 'value',
                      message: 'propertie\'s initial boolean value?',
                      choices:['true','false'],
                      default:'false',
                      filter:function(value){
                        return value == 'true' ? true : false;
                      },
                      validate: function (value) {
                        if ((/.+/).test(value)) { return true; }
                        return 'property initial value is required';
                      },
                      when:function(answers){
                        return ['boolean']
                        .includes(answers.type)
                      }
                  },
                  {
                      type:'input',
                      name:'value',
                      message:'propertie\'s initial integer value?',
                      default:0,
                      filter:function(value){
                        return Number(value);
                      },
                      validate: function (value) {
                        if ((/.+/).test(value)) { return true; }
                        return 'property initial value is required';
                      },
                      when:function(answers){
                        return ['integer']
                        .includes(answers.type)
                      }
                  },
                  {
                      type:'input',
                      name:'value',
                      message:'propertie\'s initial string value?',
                      default:'foo',
                      validate: function (value) {
                        if ((/.+/).test(value)) { return true; }
                        return 'property initial value is required';
                      },
                      when:function(answers){
                        return ['string']
                        .includes(answers.type)
                      }
                  },
                  {
                    type:'input',
                    name:'value',
                    message:'propertie\'s initial url value?',
                    default:'foo',
                    validate: function (value) {
                      if ((/.+/).test(value)) { return true; }
                      return 'property initial value is required';
                    },
                    when:function(answers){
                      return ['url']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'display',
                    message: 'Select the display type of the boolean property?',
                    choices:['button','toggle','checkbox'],
                    default:'button',
                    when:function(answers){
                      return ['boolean']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'display',
                    message: 'Select the display type of the integer property?',
                    choices:['number','meter'],
                    default:'number',
                    when:function(answers){
                      return ['integer']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'display',
                    message: 'Select the display type of the string property?',
                    choices:['text'],
                    default:'text',
                    when:function(answers){
                      return ['string']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'display',
                    message: 'Select the display type of the property?',
                    choices:['timepicker','datepicker','datetimepicker'],
                    default:'datetimepicker',
                    when:function(answers){
                      return ['time']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'units',
                    message: 'Select the display units of the property?',
                    choices:['none',
                              '%','°C',
                              'm','kg','s','A','K','mol','cd',
                              'rad','sr','Hz','N','Pa','J','W',
                              'C','V','F','Ω','S','Wb','T',
                              'H','lm','lx','Bq','Gy','sievert','katal'
                              ],
                    default:'none',
                    filter: function(value){
                      if(value == 'none'){ return null}
                      return value
                    },
                    when:function(answers){
                      return ['integer']
                      .includes(answers.type)
                    }
                  },
                  {
                    type: 'list',
                    name: 'group',
                    message: 'Select the group  of the property?',
                    choices:['info','control','settings'],
                    default:'control'
                  },

            ]
        }

        ],

        actions:function(answers){
          var actions = [];

          // Generate config.py
          actions.push({
            type: 'add',
            skipIfExists: true,
            path: 'src/products/{{typename name}}/config.py',
            templateFile: 'internals/generators/config.py.hbs'
          });

          // Generate product.py
          actions.push({
            type: 'add',
            force: true,
            path: 'src/products/{{typename name}}/product.py',
            templateFile: 'internals/generators/product.py.hbs'
          });

          // Copy in other needed mcu files
          actions.push({
            type: 'addMany',
            skipIfExists: true,
            base: 'internals/core/mcu',
            templateFiles: 'internals/core/mcu/*.py',
            destination: 'src/products/{{typename name}}/'
          });

          // Copy in other needed files
          actions.push({
            type: 'addMany',
            skipIfExists: true,
            base: 'internals/core',
            templateFiles: 'internals/core/*.py',
            destination: 'src/products/{{typename name}}/'
          });

          return actions;

        }

    });




    plop.setGenerator('flash', {
      description: 'choose the interpreter to flash to the ESP8266',
      prompts: [
        selectfirmware_prompt,
        comport_prompt
      ],
      actions:function(answers){
        var actions = [];

        process.stdout.write('Flashing firmware');
        if (shell.exec(

        'esptool.py.exe --port '+answers.comport+' --baud 460800 write_flash --flash_size=detect 0 '+answers.flashfile

        ).code !== 0) {
          shell.echo('\nError: could not flash software');
          shell.exit(1);
        }

        return actions
      }
    }
  )

  plop.setGenerator('erase', {
    description: 'erases the entire flash of the ESP8266',
    prompts: [ comport_prompt ],
    actions:function(answers){
      var actions = [];

      process.stdout.write('Erasing Flash');
      if (shell.exec(

      'esptool.py.exe --port '+answers.comport+' --baud 460800 erase_flash'

      ).code !== 0) {
        shell.echo('\nError: could not erease flash');
        shell.exit(1);
      }

      return actions
    }
  }
)    

plop.setGenerator('upload', {
  description: 'upload a product',
  prompts: [
    selectproductfolder_prompt,
    comport_prompt
  ],
  actions:function(answers){
    var actions = [];

    const filenames = []
    
    shell.ls('./src/products/'+answers.foldername).forEach(function (file) {
      filenames.push(file)
    })

    process.stdout.write('\nuploading')
    
    filenames.forEach((filename) => {
      process.stdout.write('\n'+filename)
        if (shell.exec(
          'ampy -p '+answers.comport+' -b 115200 put ./src/products/'+answers.foldername+'/'+filename
        ).code !== 0) {
          shell.echo('\nError: could not upload file', filename);
          shell.exit(1);
        }
    })

    process.stdout.write('\nstarting terminal');
    shell.exec('D:/putty/putty.exe -serial '+answers.comport+' -sercfg 115200,8,n,1,N')

    return actions
  }
}
)

plop.setGenerator('uploadfile', {
  description: 'upload a file',
  prompts: [
    selectcorefile_prompt,
    comport_prompt
  ],
  actions:function(answers){
    var actions = [];

    process.stdout.write('\nuploading '+answers.filename)

    if (shell.exec(
      'ampy -p '+answers.comport+' -b 115200 put ./internals/core/'+answers.filename
    ).code !== 0) {
      shell.echo('\nError: could not upload file', answers.filename);
      shell.exit(1);
    }

    process.stdout.write('\nstarting terminal');
    shell.exec('D:/putty/putty.exe -serial '+answers.comport+' -sercfg 115200,8,n,1,N')

    return actions
  }
}
)

plop.setGenerator('removefile', {
  description: 'remove a file from the device',
  prompts: [
    selectcorefile_prompt,
    comport_prompt
  ],
  actions:function(answers){
    var actions = [];

    process.stdout.write('\nremoving '+answers.filename)

    if (shell.exec(
      'ampy -p '+answers.comport+' -b 115200 rm '+answers.filename
    ).code !== 0) {
      shell.echo('\nError: could not upload file', answers.filename);
      shell.exit(1);
    }

    return actions
  }
}
)

plop.setGenerator('list', {
description: 'files on the device',
prompts: [ comport_prompt ],
actions:function(answers){
  var actions = [];

  if (shell.exec(
    'ampy -p '+answers.comport+' -b 115200 ls'
  ).code !== 0) {
    shell.echo('\nError: could not list files', answers.flashfile);
    shell.exit(1);
  }

  return actions
}
}
)



}; // Plot function end
