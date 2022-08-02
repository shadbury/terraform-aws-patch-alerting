resource "aws_ses_email_identity" "managed_services_email" {
  email = var.patch_alerting_recepients
}