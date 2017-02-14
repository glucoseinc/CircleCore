const tableStyle = {
  root: {
    display: 'flex',
    flexFlow: 'row nowrap',
    alignItems: 'center',
    padding: '16px 24px',
    height: 24,
    lineHeight: 1,
  },
  displayName: {
    width: '25%',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  mailAddress: {
    width: '25%',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  lastAccessAt: {
    width: '25%',
  },
  isAdmin: {
    flexGrow: 1,
  },
  moreIconMenu: {
    width: 24,
  },
}

export default tableStyle
