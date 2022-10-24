import {requestAPI} from './handler';
import {
showErrorMessage
} from '@jupyterlab/apputils';

export function initDataset(rootPath:string, template?: any) {

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
    showErrorMessage("Dataset already initialized", reason)
  });
}


