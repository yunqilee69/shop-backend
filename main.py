"""
超市后端管理系统 - 启动入口
"""
import uvicorn

if __name__ == "__main__":
    # 启动 FastAPI 应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，代码修改自动重载
    )
