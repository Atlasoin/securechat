import sys
import register
if __name__ == '__main__':
    app = register.QApplication(sys.argv)
    regui = register.RegUI()
    print("233")
    # 跳转到登录界面
    sys.exit(app.exec_())