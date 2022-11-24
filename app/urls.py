from django.urls import path


from .controllers.historycallcontroller import HistoryCallController
from .controllers.historycalldetailcontroller import HistoryCallDetailController
from .controllers.financialentitycontroller import FinancialEntityController
from .controllers.predictioncontroller import PredictionController, PredictionExportController
from .controllers.dashboardcontroller import DashboardController
from .controllers.logincontroller import LoginController
from .controllers.registercontroller import RegisterController
from .controllers.companycontroller import CompanyController
from .controllers.usercontroller import UserController
from .controllers.recoverpasswordcontroller import RecoverPasswordController
from .controllers.resetpasswordcontroller import ResetPasswordController
urlpatterns = [
    path('financial_enitities/', FinancialEntityController.as_view(), name = 'financial_enitity_list'),
    path('history_calls/', HistoryCallController.as_view(), name = 'history_call_list'),
    path('history_call_details/<int:history_call_id>', HistoryCallDetailController.as_view(), name = 'history_call_details_list'),
    path('predictions/', PredictionController.as_view(), name = 'prediction_list'),
    path('predictions/export_to_excel', PredictionExportController.as_view(), name = 'export_to_excel' ),
    path('dashboards/', DashboardController.as_view(), name = 'dashboards'),
    path('login/', LoginController.as_view(), name = 'login'),
    path('register/', RegisterController.as_view(), name = 'user_register'),
    path('companies/', CompanyController.as_view(), name = 'companies'),
    path('users/', UserController.as_view(), name = 'user_list'),
    path('recover_password/', RecoverPasswordController.as_view(), name = 'recover_password'),
    path('restart_password/<str:token>', ResetPasswordController.as_view(), name = 'restart_password'),
]