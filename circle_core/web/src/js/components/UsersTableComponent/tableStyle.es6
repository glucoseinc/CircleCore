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
    width: '20%',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  id: {
    width: '20%',
  },
  mailAddress: {
    width: '20%',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  lastAccessAt: {
    width: '20%',
  },
  isAdmin: {
    flexGrow: 1,
  },
  moreIconMenu: {
    width: 24,
  },
}

export default tableStyle
