variable "patch_alerting_recepients" {
    type        = string
    description = "email to receive patching alerts"
    default     = ""
}

variable "patch_alerting_sender" {
    type        = string
    description = "email to send patching alerts"
    default     = ""
}

variable "profile" {
    type       = string
    description = "Account to be used"
}