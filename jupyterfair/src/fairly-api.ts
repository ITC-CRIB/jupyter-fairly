import {requestAPI} from './handler';
import {
showErrorMessage
} from '@jupyterlab/apputils';

export function initDataset(rootPath:string, template?: any) {
  /**
   * Initializes a Fairly dataset
   * @param rootPath - path to dataset root directory
   * @param template - alias of template for manifest.yalm
   */

  // name of the template for manifest.yalm
  let templateMeta = '';
  if(template === '4TU.Research' || template === 'Figshare') {
    templateMeta = 'figshare';
  }
  else if (template === 'Zenodo'){
    templateMeta = 'zenodo'
  }
  else if (template == null || template === 'Default'){
    templateMeta = 'default'
  }

  requestAPI<any>('newdataset', {
    method: 'POST', 
    body: JSON.stringify({
      path: rootPath, 
      template: templateMeta
    })
  }) 
  .then(data => {
    console.log(data);
  })
  .catch(reason => {
    console.error(
      `${reason}`
    );
    // show error when manifest.yalm already exist in rootPath
    showErrorMessage("Error: Has the dataset been initilized already?", reason)
  });
}


