import React, {Component, PropTypes} from 'react'

import {Card, CardActions, CardMedia} from 'material-ui/Card'
import Chip from 'material-ui/Chip'
import {GridList, GridTile} from 'material-ui/GridList'
import Subheader from 'material-ui/Subheader'
import RaisedButton from 'material-ui/RaisedButton'


/**
 */
class ModuleInfo extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {module} = this.props

    const style = {
      tagChip: {
        display: 'inline-flex',
        margin: 2,
      },
    }

    return (
      <Card style={{margin: 4}}>
        <CardMedia>
          <GridList cellHeight="auto">
            <GridTile>
              <GridList cellHeight="auto" cols={4}>
                <GridTile>
                    <Subheader>Name</Subheader>
                </GridTile>
                <GridTile cols={3}>
                  <Subheader>{module.displayName}</Subheader>
                </GridTile>
              </GridList>
            </GridTile>
            <GridTile>
              <GridList cellHeight="auto" cols={4}>
                <GridTile>
                    <Subheader>UUID</Subheader>
                </GridTile>
                <GridTile cols={3}>
                  <Subheader>{module.uuid}</Subheader>
                </GridTile>
              </GridList>
            </GridTile>
            <GridTile cols={2}>
                <div style={{paddingLeft: 16}}>
                  Metadata
                </div>
                <GridList cellHeight="auto">
                  <GridTile>
                    <Subheader>Tags</Subheader>
                    <div style={{paddingLeft: 24}}>
                      {module.tags.map((tag) =>
                        <Chip style={style.tagChip} key={tag}>
                          {tag}
                        </Chip>
                      )}
                    </div>
                  </GridTile>
                  <GridTile>
                    <Subheader>Memo</Subheader>
                    <div style={{paddingLeft: 24}}>
                      {module.description}
                    </div>
                  </GridTile>
                </GridList>
            </GridTile>
          </GridList>
        </CardMedia>
        <CardActions>
          <RaisedButton
            label="Edit"
          />
        </CardActions>
      </Card>
    )
  }
}

export default ModuleInfo
