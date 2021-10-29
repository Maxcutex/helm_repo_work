

output "helm_chart_repository_bucket_domain_name" {
  value = "${aws_s3_bucket.helm-chart-repository.bucket_domain_name}"
}