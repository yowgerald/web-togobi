'use strict';

class FileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      files: []
    };
  }

  handleChange(e) {
    if (typeof e != 'undefined') {
      var fi = e.target;
      var files = [];
      if(fi.files.length > 0) {
        for (var i = 0; i < fi.files.length; i++) {
          var nfile = {
            id: i,
            name: fi.files.item(i).name,
            size: fi.files.item(i).size
          }
          files.push(nfile)
        }
        this.setState({
          files: files
        });
      }
    }
  }

  handleRemove(id) {
    this.setState({
      files: this.state.files.filter(f => f.id !== id)
    });
    var excluded = document.querySelector('#exclusions');
    var exs = excluded.value || '';
    excluded.value = exs + '' + (exs != '' ? ','+id : id)
  }

  render() {
    return [
      <label htmlFor="content-file" className="button" key="uploader-label">Upload File</label>,
      <input id="content-file" name="content-file" className="show-for-sr" type="file" multiple key="uploader" onChange={this.handleChange.bind(this)}/>,
      <input id="exclusions" name="exclusions" hidden key="excluded"/>,
      <ul key="file-list">
        {this.state.files.map((file) => (
          <li key={file.id}>
            <span>{file.id}..{file.name}</span>.....
            <span>{file.size}bytes</span>.....
            <button className="hollow button tiny alert" onClick={this.handleRemove.bind(this, file.id)}>remove</button>
          </li>
        ))}
      </ul>
    ]
  }
}


ReactDOM.render(<FileUpload/>, document.querySelector('#upload_container'));